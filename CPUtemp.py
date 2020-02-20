#!/usr/bin/python3

# -*- coding:utf-8 -*-

import redis
from gpiozero import CPUTemperature
from time import sleep

def sensor_lock(lock_status):
    redis_db.set('CPUtemperature_sensor_in_use', str(lock_status))

def wrtite_sensor_data_to_db():
    data = CPUTemperature()
    redis_db.set('CPUtemperature', data.temperature)
    print('CPU temperature: {0:0.0f}\xb0C'.format(data.temperature))
    sleep(1)

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

sensor_status=redis_db.get('CPUtemperature_sensor_in_use')

if  sensor_status is None:
    sensor_lock(1)
    wrtite_sensor_data_to_db()
    sensor_lock(0)

elif str(sensor_status) is '0' :
     sensor_lock(1)
     wrtite_sensor_data_to_db()
     sensor_lock(0)
else:
    print('The sensor is in use, please try again later')

