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
import fcntl
#import os
import sys
import json
import subprocess
from signal import pause

import yaml
import redis

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


class AppContext:
    def __init__(self, gpio, config, zabbix_agent, sensors, redis_db):
        self.gpio = gpio
        self.config = config
        self.zabbix_agent = zabbix_agent
        self.sensors = sensors
        self.redis_db = redis_db

        # sensors subset:
        self.bme280_config = sensors['BME280']
        self.dht_config = sensors['DHT']
        self.cputemp_config = sensors['CPU']['temp']
        self.ds18b20_config = sensors['ONE_WIRE']['DS18B20']
        self.rainfall_config = sensors['WEATHER']['RAINFALL']
        self.windspeed_config = sensors['WEATHER']['WIND']['SPEED']
        self.winddirection_config = sensors['WEATHER']['WIND']['DIRECTION']

        # gpio supsets
        self.door_sensors = {}
        self.motion_sensors = {}
        self.system_buttons = {}
        self.led_indicators = {}


class SensorContext:
    def __init__(self, app_context, sensor_name, sensor_config):
        self.app = app_context          # global AppContext
        self.name = sensor_name         # for example "id3"
        self.config = sensor_config     # config specific sensor


# --- Functions ---
def acquire_lock(lock_path="/run/lock/rpims.lock"):
    try:
        fp = open(lock_path, "w") # pylint: disable=consider-using-with
    except PermissionError:
        logger.error("Cannot open lock file %s. Check permissions.", lock_path)
        sys.exit(255)

    try:
        fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        logger.error("Another instance of RPiMS is already running. Exiting.")
        sys.exit(255)

    return fp  # keep file descriptor open!


def detect_no_alarms(ctx):
    use_door = ctx.config.get('use_door_sensor')
    use_motion = ctx.config.get('use_motion_sensor')

    # both type door and motion sensors are active
    if use_door and use_motion:
        door_values = [sensor.value for sensor in ctx.door_sensors.values()]
        motion_values = [int(not sensor.value) for sensor in ctx.motion_sensors.values()]
        return all(door_values) and all(motion_values)

    # only door sensors
    if use_door and not use_motion:
        door_values = [sensor.value for sensor in ctx.door_sensors.values()]
        return all(door_values)

    # only motion sensors
    if not use_door and use_motion:
        motion_values = [int(not sensor.value) for sensor in ctx.motion_sensors.values()]
        return all(motion_values)

    # no sensors = no alarms
    return True


def av_stream(state):
    _cmd = f'sudo systemctl {state} mediamtx.service'
    subprocess.call(_cmd, shell=True)


def hostnamectl_sh(**kwargs):
    hctldict = {
        "location": "set-location",
        "chassis": "set-chassis",
        "deployment": "set-deployment",
    }

    # set hostname
    hostname = kwargs.get('hostname')
    if hostname:
        subprocess.call([
            'sudo', 'raspi-config', 'nonint', 'do_hostname', hostname
        ])

    # use hostnamectl
    for key, action in hctldict.items():
        value = kwargs.get(key)
        if value:
            subprocess.call([
                'sudo', '/usr/bin/hostnamectl', action, value
            ])


def get_hostip():
    _cmd = 'sudo ../scripts/gethostinfo.sh'
    subprocess.call(_cmd, shell=True)


def db_connect(dbhost, dbnum):
    try:
        redis_db = redis.StrictRedis(host=dbhost, port=6379, db=str(dbnum), decode_responses=True)
        redis_db.ping()
        return redis_db
    except Exception as err:
        logger.error(err)
        logger.error("Can't connect to RedisDB host: %s", dbhost)
        sys.exit(255)


def config_load(path_to_config):
    try:
        with open(path_to_config, mode='r') as file:
            config_yaml = yaml.full_load(file)
        return config_yaml
    except Exception as err:
        logger.error(err)
        logger.error = ("Can't load RPiMS config file: %s", path_to_config)
        sys.exit(255)


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
