#!/usr/bin/python3

# -*- coding:utf-8 -*-

import w1thermsensor
import redis

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
sensor_status=redis_db.get('DS18B20_sensor_in_use')

if sensor_status is None:
    redis_db.set('DS18B20_sensor_in_use', '0')
    sensor_status=redis_db.get('DS18B20_sensor_in_use')

if str(sensor_status) is '0' :
    redis_db.set('DS18B20_sensor_in_use', '1')

    sensor = w1thermsensor.W1ThermSensor()
    ds18b20 = sensor.get_temperature()
    
    redis_db.set('Temperature', ds18b20)
    print('DS18B20 Temperature: {0:0.2f}C'.format(ds18b20))
    
    redis_db.set('DS18B20_sensor_in_use', '0')

else:
    print('The sensor is in use, please try again later')
