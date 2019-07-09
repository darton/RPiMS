#!/usr/bin/python3

# -*- coding:utf-8 -*-

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib
from luma.oled.device import sh1106
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
height = 64
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

USER_I2C = 0

if  USER_I2C == 1:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RST,GPIO.OUT)    
    GPIO.output(RST,GPIO.HIGH)
    
    serial = i2c(port=1, address=0x3c)
else:
    serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)

device = sh1106(serial, rotate=2) #sh1106  

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
            draw.text((x, top+9),     'Temperature..' + str(temperature) + '*C', font=font, fill=255)
            draw.text((x, top+18),    'Humidity.....' + str(humidity) + '%',  font=font, fill=255)
            draw.text((x, top+27),    'Pressure.....' + str(pressure) + 'hPa',  font=font, fill=255)
            draw.text((x, top+36),    'Door 1.......' + str(door_sensor_1),  font=font, fill=255)
            draw.text((x, top+45),    'Door 2.......' + str(door_sensor_2),  font=font, fill=255)
            draw.text((x, top+54),    'Door 3.......' + str(door_sensor_3),  font=font, fill=255)

except:
    print("Error")
GPIO.cleanup()
