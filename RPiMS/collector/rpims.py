#!/usr/bin/env python3

# -*- coding:utf-8 -*-
#
#  Author : Dariusz Kowalczyk
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License Version 2 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import logging
import sys
import json
from signal import pause

from system.lock import acquire_lock
from config.loader import config_load
from system.redis import db_connect
from models.context import AppContext, SensorContext
from system.services import get_hostip, hostnamectl_sh, av_stream
from sensors.bme280 import get_bme280_data
from sensors.ds18b20 import get_ds18b20_data
from sensors.dht import get_dht_data
from sensors.cputemp import get_cputemp_data
from sensors.rainfall import rainfall
from sensors.windspeed import wind_speed
from sensors.winddirection import wind_direction
from displays import serial_displays
from execution import start_process
from gpio.door import init_door_sensors, setup_door_callbacks
from gpio.motion import init_motion_sensors, setup_motion_callbacks
from gpio.buttons import init_system_buttons, setup_system_buttons_callbacks
from gpio.leds import init_led_indicators


logging.basicConfig(
    level=logging.INFO,
    format="RPiMS-collector: %(levelname)s: %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger("RPiMS-collector")

# --- Functions ---
def main():
    logger.info('')
    logger.info('# RPiMS is running #')
    logger.info('')

    redis_db = db_connect('localhost', 0)
    config_yaml = config_load('../config/rpims.yaml')

    gpio = config_yaml.get("gpio")
    config = config_yaml.get("setup")
    zabbix_agent = config_yaml.get("zabbix_agent")
    sensors = config_yaml.get("sensors")

    ctx = AppContext(gpio, config, zabbix_agent, sensors, redis_db)

    redis_db.flushdb()
    redis_db.set('rpims', json.dumps(config_yaml))

    get_hostip()
    hostnamectl_sh(**ctx.zabbix_agent)

    if ctx.config.get('verbose'):
        for k, v in ctx.config.items():
            logger.info('%s = %s', k, v)
        for k, v in ctx.zabbix_agent.items():
            logger.info('%s = %s', k, v)

    ## hardware initialization
    # door sensors – initial state + callbacks
    if ctx.config.get('use_door_sensor'):
        ctx.door_sensors = init_door_sensors(ctx)
        setup_door_callbacks(ctx)

    # motion sensors – initial state + callbacks
    if ctx.config.get('use_motion_sensor'):
        ctx.motion_sensors = init_motion_sensors(ctx)
        setup_motion_callbacks(ctx)

    # system buttons
    if ctx.config.get('use_system_buttons'):
        ctx.system_buttons = init_system_buttons(ctx)
        setup_system_buttons_callbacks(ctx)

    # led indicators
    if ctx.config.get('use_motion_led_indicator'):
        ctx.led_indicators = init_led_indicators(ctx)

    # CPU temperature sensor
    if ctx.config.get('use_cpu_sensor'):
        start_process(get_cputemp_data, ctx)

    # BME280 sensors
    if ctx.config.get('use_bme280_sensor'):
        for name, bme280 in ctx.bme280_config.items():
            if bme280.get('use'):
                sensor_ctx = SensorContext(ctx, name, bme280)
                start_process(get_bme280_data, sensor_ctx)

    # DS18B20 sensors
    if ctx.config.get('use_ds18b20_sensor'):
        start_process(get_ds18b20_data, ctx)

    # DHT sensors
    if ctx.config.get('use_dht_sensor'):
        start_process(get_dht_data, ctx)

    # Weather station
    if ctx.config.get('use_weather_station'):
        # Rainfall meter
        if ctx.rainfall_config.get('use'):
            start_process(rainfall, ctx)
        # Wind speed meter
        if ctx.windspeed_config.get('use'):
            start_process(wind_speed, ctx)
        # Wind direction meter
        if ctx.winddirection_config.get('use'):
            start_process(wind_direction, ctx)

    # Serial display
    if ctx.config.get('use_serial_display'):
        start_process(serial_displays, ctx)

    # Picamera sensor
    if ctx.config.get('use_picamera'):
        av_stream('start')
    else:
        av_stream('stop')

    pause()


# --- Main program ---
if __name__ == '__main__':
    lock = acquire_lock()
    try:
        main()
    except KeyboardInterrupt:
        logger.info('# RPiMS is stopped #')
    except Exception as err:
        logger.error(err)
        sys.exit(1)
