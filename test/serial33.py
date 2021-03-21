#!/usr/bin/env python3

from time import sleep
import serial
import redis
from rpims import db_connect

#redis_db = db_connect('localhost', 0)

mesg = 'read_bme280\r\n'

ser = serial.Serial('/dev/ttyACM0', 115200, 5)

while True:
    ser.write(mesg.encode())

    line = ser.readline()
    msg = line.decode('utf-8').split()
    if len(msg) < 3:
        break

    #redis_db.mset({'BME280_Temperature': msg[0], 'BME280_Humidity': msg[1], 'BME280_Pressure': msg[2]})
    #redis_db.expire('BME280_Temperature', 10)
    #redis_db.expire('BME280_Humidity', 10)
    #redis_db.expire('BME280_Pressure', 10)
    print(f'Temperature: {msg[0]} °C, Humidity: {msg[1]} %, Pressure: {msg[2]} hPa')
    sleep(1)

ser.close()
