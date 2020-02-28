#!/usr/bin/python3

# -*- coding:utf-8 -*-

import redis
import sys

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

if len(sys.argv) > 1:
    if sys.argv[1] == 'BME280':
        if redis_db.get('use_BME280_sensor') == '1':
            temperature = redis_db.get('BME280_Temperature')
            humidity = redis_db.get('BME280_Humidity')
            pressure = redis_db.get('BME280_Pressure')
            print('Temperature={0:0.2f};Humidity={1:0.2f};Pressure={2:0.2f};'.format(float(temperature),float(humidity),float(pressure)))
    elif sys.argv[1] == 'DS18B20':
        if redis_db.get('use_DS18B20_sensor') == '1':
            for sensor in redis_db.keys(pattern='DS18B20-*'):
                print(sensor + '={0:0.2f}'.format(float(redis_db.get(sensor))), end=';')
            print('')
    elif sys.argv[1] == 'DHT22':
        if redis_db.get('use_DHT22_sensor') == '1':
            temperature = redis_db.get('DHT22_Temperature')
            humidity = redis_db.get('DHT22_Humidity')
            print('Temperature={0:0.2f};Humidity={1:0.2f};'.format(float(temperature),float(humidity)))
    elif sys.argv[1] == 'CPUTEMP':
        temperature = redis_db.get('CPU_Temperature')
        print('CPUTemperature' + '={0:0.2f};'.format(float(temperature)))
else:
    print('You must use one parameter from list BME280, DS18B20, DHT22, CPUTEMP')
