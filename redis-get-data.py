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
sensors = json.loads(redis_db.get('sensors'))

def print_help():
    print('You must use one parameter from list BME280 id (where id is 1, 2 or 3), DHT, CPUTEMP, DS18B20, ds18b20 address')


if len(sys.argv) > 1:
    if sys.argv[1] == 'BME280':
        if config['use_BME280_sensor'] is True:
            if len(sys.argv) == 3:
                bme_id = sys.argv[2]
                if redis_db.exists(f'id{bme_id}_BME280_Temperature') and redis_db.exists(f'id{bme_id}_BME280_Humidity') and redis_db.exists(f'id{bme_id}_BME280_Pressure'):
                    temperature = redis_db.get(f'id{bme_id}_BME280_Temperature')
                    humidity = redis_db.get(f'id{bme_id}_BME280_Humidity')
                    pressure = redis_db.get(f'id{bme_id}_BME280_Pressure')
                    print('Temperature={0:0.2f};Humidity={1:0.2f};Pressure={2:0.2f};'.format(float(temperature),float(humidity),float(pressure)))
            else: print_help()

    elif sys.argv[1] == 'DS18B20':
        if config['use_DS18B20_sensor'] is True:
            ds18b20_sensors = []
            for item in redis_db.smembers('DS18B20_sensors'):
                ds18b20_sensors.append(item)
            ds18b20_sensors.sort()
            for sensor in ds18b20_sensors:
                if redis_db.exists(sensor):
                    print(sensor + '={0:0.2f}'.format(float(redis_db.get(sensor))), end=';')
            print('')

    elif sys.argv[1] == 'ds18b20':
        if config['use_DS18B20_sensor'] is True:
            if len(sys.argv) == 3:
                onewire_addr = sys.argv[2]
                if redis_db.exists(onewire_addr):
                    print(redis_db.get(onewire_addr))
            else: print_help()

    elif sys.argv[1] == 'DHT':
        if config['use_DHT_sensor'] is True:
            if redis_db.exists('DHT_Temperature') and redis_db.exists('DHT_Humidity'):
                temperature = redis_db.get('DHT_Temperature')
                humidity = redis_db.get('DHT_Humidity')
                print('Temperature={0:0.2f};Humidity={1:0.2f};'.format(float(temperature),float(humidity)))

    elif sys.argv[1] == 'CPUTEMP':
        if config['use_CPU_sensor'] is True:
            if redis_db.exists('CPU_Temperature'):
                temperature = redis_db.get('CPU_Temperature')
                print('CPUTemperature' + '={0:0.2f};'.format(float(temperature)))
else:
    print_help()

