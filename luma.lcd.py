#!/usr/bin/python

# -*- coding:utf-8 -*-

#https://luma-lcd.readthedocs.io/en/latest/python-usage.html

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.core import lib
from luma.lcd.device import st7735
import RPi.GPIO as GPIO

import time
import redis
import socket

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

# Load default font.
font = ImageFont.load_default()

width = 128
height = 128


# First define some constants to allow easy resizing of shapes.
padding = 3
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 2


serial = spi(device=0, port=0, bus_speed_hz = 16000000, transfer_size = 4096, gpio_DC = 25, gpio_RST = 27)
device = st7735(serial)

try:
    #font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf', 10)
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
    while True:
        with canvas(device) as draw:
            hostname = socket.gethostname()
            hostip = socket.gethostbyname(hostname)
 
#get data from redis db
            temperature = round(float(redis_db.get('Temperature')),1)
            humidity = round(float(redis_db.get('Humidity')),1)
            pressure = round(float(redis_db.get('Pressure')),1)
            door_sensor_1 = redis_db.get('door_sensor_1')
            door_sensor_2 = redis_db.get('door_sensor_2')
            door_sensor_3 = redis_db.get('door_sensor_3')

#draw on lcd
            draw.text((x, top),       'IP:' + str(hostip), font=font, fill="red")
            draw.text((x, top+20),    'Temperature..' + str(temperature) + '*C', font=font, fill="red")
            draw.text((x, top+31),    'Humidity.....' + str(humidity) + '%',  font=font, fill="red")
            draw.text((x, top+41),    'Pressure.....' + str(pressure) + 'hPa',  font=font, fill="red")
            draw.text((x, top+61),    'Door 1.......' + str(door_sensor_1),  font=font, fill="red")
            draw.text((x, top+71),    'Door 2.......' + str(door_sensor_2),  font=font, fill="red")
            draw.text((x, top+81),    'Door 3.......' + str(door_sensor_3),  font=font, fill="red")

except KeyboardInterrupt:
    print("Error")
GPIO.cleanup()
