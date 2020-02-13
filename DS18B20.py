#!/usr/bin/python3

# -*- coding:utf-8 -*-

import w1thermsensor
import redis

sensor = w1thermsensor.W1ThermSensor()
ds18b20 = sensor.get_temperature()
print('DS18B20 temperature: {}C'.format(ds18b20))

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
redis_db.set('Temperature', ds18b20)
