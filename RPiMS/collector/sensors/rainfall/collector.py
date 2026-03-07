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
import math
from gpiozero import Button

logger = logging.getLogger(__name__)


def rainfall(ctx):
    # configuration
    verbose = ctx.config.get('verbose')
    sensor_pin = ctx.rainfall_config.get('sensor_pin')
    acquisition_time = ctx.rainfall_config.get('acquisition_time')
    aggregation_time = ctx.rainfall_config.get('agregation_time')

    BUCKET_SIZE = 0.2794  # mm per tilt
    bucket_counter = 0
    rainfalls = []

    # helper functions
    def bucket_tipped():
        nonlocal bucket_counter
        bucket_counter += 1

    def reset_bucket_counter():
        nonlocal bucket_counter
        bucket_counter = 0

    def calculate_rainfall():
        return round(bucket_counter * BUCKET_SIZE, 0)

    # sensor initialisation
    rain_sensor = Button(sensor_pin)
    rain_sensor.when_pressed = bucket_tipped

    # setting initial values in Redis
    ctx.redis_db.hset('WEATHER', 'daily_rainfall', 0)
    ctx.redis_db.hset('WEATHER', 'rainfall', 0)

    # main loop
    while True:
        start_time = time()

        while time() - start_time <= acquisition_time:
            reset_bucket_counter()
            sleep(acquisition_time)

            rainfall_value = calculate_rainfall()

            # limit on the list length
            if len(rainfalls) == (aggregation_time / acquisition_time):
                rainfalls.clear()

            rainfalls.append(rainfall_value)

        daily_rainfall = round(math.fsum(rainfalls), 1)

        if verbose:
            logger.info("Rainfall: %s mm, Daily rainfall: %s mm", rainfall_value, daily_rainfall)

        ctx.redis_db.hset('WEATHER', 'daily_rainfall', daily_rainfall)
        ctx.redis_db.hset('WEATHER', 'rainfall', rainfall_value)
