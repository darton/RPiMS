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

"""
The script retrieves sensor data from the Redis database for the Zabbix agent
"""

import sys
import re
import json
import redis

try:
    redis_db = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_db.ping()
except Exception:
    sys.exit(0)

rpims = json.loads(redis_db.get('rpims'))
config = rpims['setup']


def print_help():
    """Helper function"""
    options = [
        "idn_BME280 (where n is 1, 2, 3)",
        "DHT",
        "CPUTEMP",
        "DS18B20",
        "ds18b20 address",
    ]

    print("You must use one parameter from the list:")
    for opt in options:
        print(" ", opt)

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if re.fullmatch(r"id[123]_BME280", arg):
         if config['use_bme280_sensor'] is True:
            if len(sys.argv) == 2:
                key = sys.argv[1]
                if redis_db.exists(key):
                    data = redis_db.hgetall(key)
                    temperature = data['temperature']
                    humidity = data['humidity']
                    pressure = data['pressure']
                    print(
                            f"Temperature={float(temperature):0.2f};"
                            f"Humidity={float(humidity):0.2f};"
                            f"Pressure={float(pressure):0.2f};"
                         )
            else:
                print_help()

    elif sys.argv[1] == 'DS18B20':
        if config['use_ds18b20_sensor'] is True:
            ds18b20_sensors = redis_db.hgetall('DS18B20')
            for sensor_id, sensor_value in ds18b20_sensors.items():
                print(f"{sensor_id}={float(sensor_value):0.2f}", end=';')

    elif sys.argv[1] == 'ds18b20':
        if config['use_ds18b20_sensor'] is True:
            if len(sys.argv) == 3:
                onewire_addr = sys.argv[2]
                ds18b20_sensors = redis_db.hgetall('DS18B20')
                if ds18b20_sensors[onewire_addr]:
                    print(ds18b20_sensors[onewire_addr])
            else:
                print_help()

    elif sys.argv[1] == 'DHT':
        if config['use_dht_sensor'] is True:
            if redis_db.exists('DHT'):
                dht = redis_db.hgetall('DHT')
                temperature = dht['temperature']
                humidity = dht['humidity']
                print(f"Temperature={float(temperature):0.2f};Humidity={float(humidity):0.2f};")

    elif sys.argv[1] == 'CPUTEMP':
        if config['use_cpu_sensor'] is True:
            if redis_db.exists('CPU_Temperature'):
                temperature = redis_db.get('CPU_Temperature')
                print(f"CPUTemperature={float(temperature):0.2f};")
else:
    print_help()
