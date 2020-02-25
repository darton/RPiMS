#!/usr/bin/python3

import redis

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

for sensor in redis_db.keys(pattern='DS18B20-*'):
    print(sensor + '={0:0.2f}'.format(float(redis_db.get(sensor))), end=';')
