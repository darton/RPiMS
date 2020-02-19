#!/usr/bin/python3

# -*- coding:utf-8 -*-

import redis
from gpiozero import CPUTemperature

def sensor_lock(lock_status):
    redis_db.set('BME280_sensor_in_use', str(lock_status))


def wrtite_sensor_data_to_db():
    cpu = CPUTemperature()
    redis_db.set('Temperature', data.temperature)  
    print('CPU temperature: {0:0.0f}C'.format(cpu.temperature))

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
redis_db.set('CPUtemperature', cpu.temperature)
