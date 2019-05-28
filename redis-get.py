#!/usr/bin/python3

import redis

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

temperature = redis_db.get('Humidity')
humidity = redis_db.get('Temperature')

print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(float(temperature), float(humidity)))

