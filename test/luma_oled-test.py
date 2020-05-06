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

#GPIO.setwarnings(False)

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

hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)



if  USER_I2C == 1:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RST,GPIO.OUT)
    GPIO.output(RST,GPIO.HIGH)

    serial = i2c(port=1, address=0x3c)
else:
    serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 24, gpio_RST = 25)

device = sh1106(serial, rotate=2) #sh1106

try:
    while True:
        with canvas(device) as draw:
            temperature = 23.0
            humidity = 48.0
            pressure = 1024.0
            door_sensor_1 = "open"
            door_sensor_2 = "open"
            door_sensor_3 = "open"
            draw.text((x, top),       'IP:' + str(hostip), font=font, fill=255)
            draw.text((x, top+9),     'Temperature..' + str(temperature) + '*C', font=font, fill=255)
            draw.text((x, top+18),    'Humidity.....' + str(humidity) + '%',  font=font, fill=255)
            draw.text((x, top+27),    'Pressure.....' + str(pressure) + 'hPa',  font=font, fill=255)
            draw.text((x, top+36),    'Door 1.......' + str(door_sensor_1),  font=font, fill=255)
            draw.text((x, top+45),    'Door 2.......' + str(door_sensor_2),  font=font, fill=255)
            draw.text((x, top+54),    'Door 3.......' + str(door_sensor_3),  font=font, fill=255)
    sleep(0.1)
except Exception as err:
    print(err)
GPIO.cleanup()
