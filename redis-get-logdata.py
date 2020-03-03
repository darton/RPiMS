#!/usr/bin/python3

import redis
import datetime
from time import sleep
from pid import PidFile

with PidFile(piddir='/tmp/'):
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
    while True:
        temperature = redis_db.get('BME280_Temperature')
        humidity = redis_db.get('BME280_Humidity')
        pressure = redis_db.get('BME280_Pressure')
        f = open("/var/tmp/sensor.log", "a")
        f.write(str(datetime.datetime.now()) + ' Temp={0:0.1f}\xb0C Humidity={1:0.1f}% Pressure={2:0.1f}hPa' .format(float(temperature),float(humidity),float(pressure)) + '\n' )
        f.close()
        sleep(60)
