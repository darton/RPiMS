#!/usr/bin/python3

import redis
import datetime

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

temperature = redis_db.get('Temperature')
humidity = redis_db.get('Humidity')

f = open("/var/tmp/dht22.log", "a")
f.write( str(datetime.datetime.now()) + ' Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(float(temperature), float(humidity))  + '\n' )
f.close()

