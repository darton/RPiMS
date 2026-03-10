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
from signal import pause
import json
from config.loader import config_load
from system.redis_db import db_connect
from models.context import AppContext
from system.services import get_hostip, hostnamectl_sh, av_stream
from core.hardware_init import init_hardware
from core.sensor_startup import start_sensors

logger = logging.getLogger("RPiMS-collector")

def run_collector():
    redis_db = db_connect('localhost', 0)
    config_yaml = config_load('../config/rpims.yaml')

    ctx = AppContext(
        gpio=config_yaml.get("gpio"),
        config=config_yaml.get("setup"),
        zabbix_agent=config_yaml.get("zabbix_agent"),
        sensors=config_yaml.get("sensors"),
        redis_db=redis_db
    )

    redis_db.flushdb()
    redis_db.set('rpims', json.dumps(config_yaml))

    get_hostip()
    hostnamectl_sh(**ctx.zabbix_agent)

    init_hardware(ctx)
    start_sensors(ctx)

    if ctx.config.get('use_picamera'):
        av_stream('start')
    else:
        av_stream('stop')

    pause()

