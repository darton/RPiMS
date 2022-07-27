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

rpims = json.loads(redis_db.get('rpims'))
config = rpims['setup']


def print_help():
    print('You must use one parameter from list BME280 id (where id is 1, 2 or 3), DHT, CPUTEMP, DS18B20, ds18b20 address')


if len(sys.argv) > 1:
    if sys.argv[1] == 'BME280':
        if config['use_bme280_sensor'] is True:
            if len(sys.argv) == 3:
                bme_id = sys.argv[2]
                if redis_db.exists(f'id{bme_id}_BME280'):
                    _bme280 = redis_db.hgetall(f'id{bme_id}_BME280')
                    temperature = _bme280['temperature']
                    humidity = _bme280['humidity']
                    pressure = _bme280['pressure']
                    print('Temperature={0:0.2f};Humidity={1:0.2f};Pressure={2:0.2f};'.format(float(temperature),float(humidity),float(pressure)))
            else: print_help()

    elif sys.argv[1] == 'DS18B20':
        if config['use_ds18b20_sensor'] is True:
            ds18b20_sensors = redis_db.hgetall('DS18B20')
            for sensor_id, sensor_value in ds18b20_sensors.items():
              print(sensor_id + '={0:0.2f}'.format(float(sensor_value)), end=';')

    elif sys.argv[1] == 'ds18b20':
        if config['use_ds18b20_sensor'] is True:
            if len(sys.argv) == 3:
                onewire_addr = sys.argv[2]
                ds18b20_sensors = redis_db.hgetall('DS18B20')
                if ds18b20_sensors[onewire_addr]:
                    print(ds18b20_sensors[onewire_addr])
            else: print_help()

    elif sys.argv[1] == 'DHT':
        if config['use_dht_sensor'] is True:
            if redis_db.exists('DHT'):
                dht = redis_db.hgetall('DHT')
                temperature = dht['temperature']
                humidity = dht['humidity']
                print('Temperature={0:0.2f};Humidity={1:0.2f};'.format(float(temperature),float(humidity)))

    elif sys.argv[1] == 'CPUTEMP':
        if config['use_cpu_sensor'] is True:
            if redis_db.exists('CPU_Temperature'):
                temperature = redis_db.get('CPU_Temperature')
                print('CPUTemperature' + '={0:0.2f};'.format(float(temperature)))
else:
    print_help()

