#!/usr/bin/env python3

# -*- coding:utf-8 -*-
#
#  Author : Dariusz Kowalczyk
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License Version 2 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

import redis
import json
import sys

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
config = json.loads(redis_db.get('config'))

if len(sys.argv) > 1:
    if sys.argv[1] == 'BME280':
        if config['use_BME280_sensor'] is True:
            temperature = redis_db.get('BME280_Temperature')
            humidity = redis_db.get('BME280_Humidity')
            pressure = redis_db.get('BME280_Pressure')
            print('Temperature={0:0.2f};Humidity={1:0.2f};Pressure={2:0.2f};'.format(float(temperature),float(humidity),float(pressure)))

    elif sys.argv[1] == 'DS18B20':
        if config['use_DS18B20_sensor'] is True:
            ds18b20_sensors = []
            for item in redis_db.smembers('DS18B20_sensors'):
                ds18b20_sensors.append(item)
            ds18b20_sensors.sort()
            for sensor in ds18b20_sensors:
                print(sensor + '={0:0.2f}'.format(float(redis_db.get(sensor))), end=';')
            print('')

    elif sys.argv[1] == 'ds18b20':
        wire_id = sys.argv[2]
        if config['use_DS18B20_sensor'] is True:
            print(redis_db.get(wire_id))

    elif sys.argv[1] == 'DHT':
        if config['use_DHT_sensor'] is True:
            temperature = redis_db.get('DHT_Temperature')
            humidity = redis_db.get('DHT_Humidity')
            print('Temperature={0:0.2f};Humidity={1:0.2f};'.format(float(temperature),float(humidity)))

    elif sys.argv[1] == 'CPUTEMP':
        if config['use_CPU_sensor'] is True:
            temperature = redis_db.get('CPU_Temperature')
            print('CPUTemperature' + '={0:0.2f};'.format(float(temperature)))
else:
    print('You must use one parameter from list BME280, DHT22, CPUTEMP, DS18B20, ds18b20 address')
