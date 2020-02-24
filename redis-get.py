#!/usr/bin/python3

# -*- coding:utf-8 -*-

import redis

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

temperature = redis_db.get('Temperature')
humidity = redis_db.get('Humidity')
pressure = redis_db.get('Pressure')

#print(temperature,humidity,pressure)
print('{0:0.2f};{1:0.2f};{2:0.2f};'.format(float(temperature),float(humidity),float(pressure)))
