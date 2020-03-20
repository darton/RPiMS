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

from w1thermsensor import W1ThermSensor
from time import sleep
import redis

def sensor_lock(lock_status):
    redis_db.set('DS18B20_sensor_in_use', str(lock_status))

def write_sensors_data_to_db():
    sensor_lock(1)
    sensorslist = W1ThermSensor.get_available_sensors([W1ThermSensor.THERM_SENSOR_DS18B20])
    for sensor in sensorslist:
        sleep(0.5)
        print("Sensor %s temperature %.2f"%(sensor.id,sensor.get_temperature()),"\xb0C")
        redis_db.set('DS18B20-' + sensor.id, sensor.get_temperature())
    sensor_lock(0)

try:
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
    sensor_status=redis_db.get('DS18B20_sensor_in_use')
    if str(sensor_status) is '0' or sensor_status is None:
        write_sensors_data_to_db()
    else:
        print('The sensor is in use, please try again later')
except (KeyboardInterrupt, SystemExit):
    sensor_lock(0)
