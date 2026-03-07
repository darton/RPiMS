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
import sys

logger = logging.getLogger(__name__)

def wind_direction(ctx):
    # configuration
    verbose = ctx.config.get('verbose')
    acquisition_time = ctx.winddirection_config.get('acquisition_time')
    adc_type = ctx.winddirection_config.get('adc_type')
    adc_input = ctx.winddirection_config.get('adc_input')
    reference_input = ctx.winddirection_config.get('reference_voltage_adc_input')

    # initial values
    ctx.redis_db.hset('WEATHER', 'wind_direction', 0)
    ctx.redis_db.hset('WEATHER', 'average_wind_direction', 0)

    # resistance and angle maps
    direction_mapr = {
        "N": 5080, "NNE": 5188, "NE": 6417, "ENE": 6253,
        "E": 17419, "ESE": 9380, "SE": 11613, "SSE": 6968,
        "S": 8129, "SSW": 5419, "SW": 5542, "W": 4781,
        "NW": 4977, "NNW": 4877,
    }

    direction_mapa = {
        "N": 0, "NNE": 22.5, "NE": 45, "ENE": 67.5,
        "E": 90, "ESE": 112.5, "SE": 135, "SSE": 157.5,
        "S": 180, "SSW": 202.5, "SW": 225, "W": 270,
        "NW": 315, "NNW": 337.5,
    }

    # constant values
    r1 = 4690
    uin = 5.2
    uout = 0

    # auxiliary function for calculating the average direction
    def get_average(angles):
        sin_sum = sum(math.sin(math.radians(a)) for a in angles)
        cos_sum = sum(math.cos(math.radians(a)) for a in angles)

        s = sin_sum / len(angles)
        c = cos_sum / len(angles)

        arc = math.degrees(math.atan(s / c))

        if s > 0 and c > 0:
            avg = arc
        elif c < 0:
            avg = arc + 180
        elif s < 0 < c:
            avg = arc + 360
        else:
            avg = 0

        return 0 if avg == 360 else avg

    # main loop
    while True:
        start_time = time()
        angles = []

        while time() - start_time <= acquisition_time:
            try:
                # ADC selection
                if adc_type == 'AutomationPhat':
                    from sensors.adc import adc_automationphat
                    adc_values = adc_automationphat()
                elif adc_type == 'STM32F030':
                    from sensors.adc import adc_stm32f030
                    adc_values = adc_stm32f030()
                elif adc_type == 'ADS1115':
                    from sensors.adc import adc_ads1115
                    adc_values = adc_ads1115()
                else:
                    logger.error("Unknown ADC type: %s", adc_type)
                    sleep(1)
                    continue
            except Exception as err:
                logger.error(err)
                logger.error('ADC not detected')
                sys.exit(1)

            # selection of the measurement channel
            uout = round(adc_values[adc_input - 1], 1)
            uin = round(adc_values[reference_input - 1], 1)

            # calculation of resistance R2
            if uin != uout and uin != 0:
                r2 = int(r1 / (1 - uout / uin))
            else:
                continue

            # matching resistance to direction
            for key, ref_r in direction_mapr.items():
                if ref_r * 0.995 <= r2 <= ref_r * 1.005:
                    angles.append(direction_mapa[key])
                    ctx.redis_db.hset('WEATHER', 'wind_direction', key)

        # calculation of the average direction
        if angles:
            avg_dir = int(round(get_average(angles), 0))
            ctx.redis_db.hset('WEATHER', 'average_wind_direction', avg_dir)
            if verbose:
                logger.info('Average Wind Direction: %s', avg_dir)
