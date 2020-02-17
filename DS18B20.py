#!/usr/bin/python3

# -*- coding:utf-8 -*-

from w1thermsensor import W1ThermSensor
import redis


def sensor_lock(lock_status):
    redis_db.set('DS18B20_sensor_in_use', str(lock_status))

def wrtite_sensor_data_to_db():
    sensor = W1ThermSensor()
    redis_db.set('Temperature', sensor.get_temperature())
    print('DS18B20 Temperature: {0:0.2f}C'.format(sensor.get_temperature()))

def wrtite_sensors_data_to_db():
    for sensor in W1ThermSensor.get_available_sensors([W1ThermSensor.THERM_SENSOR_DS18B20]):
        print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
        redis_db.set('DS18B20_' + sensor.id, sensor.get_temperature())


redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

sensor_status=redis_db.get('DS18B20_sensor_in_use')

if sensor_status is None:
    sensor_lock(1)
    wrtite_sensors_data_to_db()
    sensor_lock(0)

elif str(sensor_status) is '0' :
    sensor_lock(1)
    wrtite_sensors_data_to_db()
    sensor_lock(0)

else:
    print('The sensor is in use, please try again later')
