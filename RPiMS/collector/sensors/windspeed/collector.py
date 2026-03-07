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
from time import sleep, time
import statistics
from gpiozero import Button

logger = logging.getLogger(__name__)


def wind_speed(ctx):
    verbose = ctx.config.get('verbose')

    sensor_pin = ctx.windspeed_config.get('sensor_pin')
    acquisition_time = ctx.windspeed_config.get('acquisition_time')
    aggregation_time = ctx.windspeed_config.get('agregation_time')

    ANEMOMETER_FACTOR = 1.18

    anemometer_pulse = 0
    wind_speeds = []
    average_wind_speeds = []
    daily_wind_gusts = []

    # helper functions
    def anemometer_pulse_counter():
        nonlocal anemometer_pulse
        anemometer_pulse += 1

    def reset_anemometer_pulse_counter():
        nonlocal anemometer_pulse
        anemometer_pulse = 0

    def calculate_speed():
        rotations = anemometer_pulse / 2
        return round(ANEMOMETER_FACTOR * rotations * 2.4 / acquisition_time, 1)

    # sensors initialisation
    wind_speed_sensor = Button(sensor_pin)
    wind_speed_sensor.when_pressed = anemometer_pulse_counter

    # initial values
    init_values = {
        'wind_speed': 0,
        'wind_gust': 0,
        'daily_wind_gust': 0,
        'average_wind_speed': 0,
        'daily_average_wind_speed': 0
    }
    ctx.redis_db.hset('WEATHER', mapping=init_values)

    # main loop
    while True:
        start_time = time()

        while time() - start_time <= acquisition_time:
            reset_anemometer_pulse_counter()
            sleep(acquisition_time)

            speed = calculate_speed()
            ctx.redis_db.hset('WEATHER', 'wind_speed', speed)

            # short-term aggregation
            if len(wind_speeds) == (aggregation_time / acquisition_time):
                wind_speeds.pop(0)

            wind_speeds.append(speed)

        # widn gust
        wind_gust = max(wind_speeds)
        ctx.redis_db.hset('WEATHER', 'wind_gust', wind_gust)

        # daily wind gust
        if len(daily_wind_gusts) == (86400 / acquisition_time):
            daily_wind_gusts.pop(0)

        daily_wind_gusts.append(wind_gust)
        daily_gust = max(daily_wind_gusts)
        ctx.redis_db.hset('WEATHER', 'daily_wind_gust', daily_gust)

        # average speed
        avg_speed = round(statistics.mean(wind_speeds), 1)
        ctx.redis_db.hset('WEATHER', 'average_wind_speed', avg_speed)

        # average daily wind speed
        if len(average_wind_speeds) == (86400 / aggregation_time):
            average_wind_speeds.pop(0)

        average_wind_speeds.append(avg_speed)
        daily_avg_speed = round(statistics.mean(average_wind_speeds), 1)
        ctx.redis_db.hset('WEATHER', 'daily_average_wind_speed', daily_avg_speed)

        if verbose:
            logger.info(
                "Wind speed: %s km/h, "
                "Wind gust: %s km/h, "
                "Daily wind gust: %s km/h, "
                "Average wind speed: %s km/h, "
                "Daily average wind speed: %s km/h",
                speed,
                wind_gust,
                daily_gust,
                avg_speed,
                daily_avg_speed,
            )
