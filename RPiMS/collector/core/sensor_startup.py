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

from execution import start_process
from sensors.bme280 import get_bme280_data
from sensors.ds18b20 import get_ds18b20_data
from sensors.dht import get_dht_data
from sensors.cputemp import get_cputemp_data
from sensors.rainfall import rainfall
from sensors.windspeed import wind_speed
from sensors.winddirection import wind_direction
from models.context import SensorContext

def start_sensors(ctx):
    if ctx.config.get('use_cpu_sensor'):
        start_process(get_cputemp_data, ctx)

    if ctx.config.get('use_bme280_sensor'):
        for name, bme in ctx.bme280_config.items():
            if bme.get('use'):
                start_process(get_bme280_data, SensorContext(ctx, name, bme))

    if ctx.config.get('use_ds18b20_sensor'):
        start_process(get_ds18b20_data, ctx)

    if ctx.config.get('use_dht_sensor'):
        start_process(get_dht_data, ctx)

    if ctx.config.get('use_weather_station'):
        if ctx.rainfall_config.get('use'):
            start_process(rainfall, ctx)
        if ctx.windspeed_config.get('use'):
            start_process(wind_speed, ctx)
        if ctx.winddirection_config.get('use'):
            start_process(wind_direction, ctx)
