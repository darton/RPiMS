#!/usr/bin/python

# -*- coding:utf-8 -*-

#https://luma-lcd.readthedocs.io/en/latest/python-usage.html
    
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.core import lib
from luma.oled.device import ST7735
import RPi.GPIO as GPIO

import time
import redis
import socket

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Load default font.
font = ImageFont.load_default()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = 128
height = 128
image = Image.new('1', (width, height))

# First define some constants to allow easy resizing of shapes.
padding = 0
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

RST = 25
CS = 8      
DC = 24

serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 25, gpio_RST = 27)
device = ST7735(serial, rotate=1) 

try:
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
            #draw on oled
            draw.text((x, top),       'IP:' + str(hostip), font=font, fill=255)
            draw.text((x, top+9),     'Temperature..' + str(temperature) + '*C', font=font, fill="black")
            draw.text((x, top+18),    'Humidity.....' + str(humidity) + '%',  font=font, fill="red")
            draw.text((x, top+27),    'Pressure.....' + str(pressure) + 'hPa',  font=font, fill="blue")
            draw.text((x, top+36),    'Door 1.......' + str(door_sensor_1),  font=font, fill="black")
            draw.text((x, top+45),    'Door 2.......' + str(door_sensor_2),  font=font, fill="black")
            draw.text((x, top+54),    'Door 3.......' + str(door_sensor_3),  font=font, fill="black")

except:
    print("Error")
GPIO.cleanup()
