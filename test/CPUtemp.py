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

import redis
from gpiozero import CPUTemperature

def sensor_lock(lock_status):
    redis_db.set('CPUtemperature_sensor_in_use', str(lock_status))

def wrtite_sensor_data_to_db():
    sensor_lock(1)
    data = CPUTemperature()
    redis_db.set('CPU_Temperature', data.temperature)   
    #print('CPU temperature: {0:0.0f}\xb0C'.format(data.temperature))
    print('CPU temperature: {0:0.1f}'.format(data.temperature),chr(176)+'C',sep='')
    sensor_lock(0)


redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
sensor_status=redis_db.get('CPUtemperature_sensor_in_use')
if str(sensor_status) is '0' or sensor_status is None:
     wrtite_sensor_data_to_db()
else:
    print('The sensor is in use, please try again later')
