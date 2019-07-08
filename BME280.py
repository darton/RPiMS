#!/usr/bin/python3

import smbus2
import bme280
import redis

port = 1
address = 0x77
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
redis_db.set('Humidity', data.humidity)
redis_db.set('Temperature', data.temperature)
redis_db.set('Pressure', data.pressure)
