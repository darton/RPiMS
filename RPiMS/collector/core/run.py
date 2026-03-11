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
from system.services import get_hostinfo, set_hostnamectl, video_service, zabbix_service
from core.hardware_init import init_hardware
from core.sensor_startup import start_sensors
from core.display_startup import start_display

logger = logging.getLogger("RPiMS-collector")

def run_collector():
    redis_db = db_connect('localhost', 0)
    config_yaml = config_load('../config/rpims.yaml')

    ctx = AppContext(
        gpio=config_yaml.get("gpio"),
        config=config_yaml.get("setup"),
        zabbix_agent=config_yaml.get("zabbix_agent"),
        sensors=config_yaml.get("sensors"),
        serial_bus_display=config_yaml.get("serial_bus_display"),
        redis_db=redis_db
    )

    #redis_db.flushdb() #flush redis_db for development
    #redis_db.set('rpims', json.dumps(config_yaml))#load config to redis_db in json format
    redis_db.set('rpims', json.dumps(config_yaml), nx=True)#load config to redis_db in json format when no loaded

    get_hostinfo()
    set_hostnamectl(**ctx.zabbix_agent)

    init_hardware(ctx)
    start_sensors(ctx)
    start_display(ctx)

    if ctx.config.get('use_picamera'):
        video_service('restart')
    else:
        video_service('stop')

    if ctx.config.get('use_zabbix_sender'):
        zabbix_service('restart')
    else:
        zabbix_service('stop')

    pause()
