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
from time import sleep
from w1thermsensor import W1ThermSensor

logger = logging.getLogger(__name__)


def get_ds18b20_data(ctx):
    verbose = ctx.config.get('verbose')
    read_interval = ctx.ds18b20_config.get('read_interval')

    try:
        while True:
            sensors = W1ThermSensor.get_available_sensors()

            for sensor in sensors:
                temperature = sensor.get_temperature()
                ctx.redis_db.hset('DS18B20', sensor.id, temperature)

                if verbose:
                    logger.info("Sensor %s temperature %.2f°C",sensor.id,temperature,)

            # data expiration time setting
            expire_time = 10 if read_interval < 5 else read_interval * 2
            ctx.redis_db.expire('DS18B20', expire_time)

            sleep(read_interval)

    except Exception as err:
        logger.info('Problem with sensor DS18B20: %s', err)
