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
from gpiozero import CPUTemperature

logger = logging.getLogger(__name__)

def get_cputemp_data(ctx):
    verbose = ctx.config.get('verbose')
    read_interval = ctx.cputemp_config.get('read_interval')

    try:
        while True:
            data = CPUTemperature()
            ctx.redis_db.set('CPU_Temperature', data.temperature)
            ctx.redis_db.expire('CPU_Temperature', read_interval * 2)

            if verbose:
                logger.info("CPU temperature: %.1f%sC", data.temperature, chr(176))
            sleep(read_interval)

    except Exception as err:
        logger.info('Problem with CPU sensor: %s',err)

