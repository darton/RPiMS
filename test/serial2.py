#!/usr/bin/env python3

import time
import serial
import redis
from rpims import db_connect

redis_db = db_connect('localhost', 0)

def serial_data(port, baudrate):
    ser = serial.Serial(port, baudrate)

    while True:
        yield ser.readline()

    ser.close()


for line in serial_data('/dev/ttyACM0', 38400):
    msg = line.decode('utf-8').split()
    print(f'Temperature: {msg[0]} °C, Humidity: {msg[1]} %, Pressure: {msg[2]} hPa')
    redis_db.mset({'BME280_Temperature': msg[0], 'BME280_Humidity': msg[1], 'BME280_Pressure': msg[2]})
    redis_db.expire('BME280_Temperature', 10)
    redis_db.expire('BME280_Humidity', 10)
    redis_db.expire('BME280_Pressure', 10)
