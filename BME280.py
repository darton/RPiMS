#!/usr/bin/python3

# -*- coding:utf-8 -*-

import smbus2
import bme280
import redis
from time import sleep

port = 1
address = 0x77
bus = smbus2.SMBus(port)


def sensor_lock(lock_status):
    redis_db.set('BME280_sensor_in_use', str(lock_status))

def wrtite_sensor_data_to_db():
    sensor_lock(1)
    calibration_params = bme280.load_calibration_params(bus, address)
    data = bme280.sample(bus, address, calibration_params)

    redis_db.set('Humidity', data.humidity)
    redis_db.set('Temperature', data.temperature)
    redis_db.set('Pressure', data.pressure)

    print('Humidity: {0:0.0f}%'.format(data.humidity))
    print('Temperature: {0:0.1f}\xb0C'.format(data.temperature))
    print('Pressure: {0:0.0f}hPa'.format(data.pressure))

    sleep(1)
    sensor_lock(0)


redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
sensor_status=redis_db.get('BME280_sensor_in_use')
if str(sensor_status) is '0' or sensor_status is None:
     wrtite_sensor_data_to_db()
else:
    print('The sensor is in use, please try again later')

