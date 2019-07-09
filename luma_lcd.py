#!/usr/bin/python3

# -*- coding:utf-8 -*-

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
padding = 0
top = padding
bottom = height-padding

# Move left to right keeping track of the current x position for drawing shapes.
x = 10

serial = spi(device=0, port=0, bus_speed_hz = 16000000, transfer_size = 4096, gpio_DC = 25, gpio_RST = 27)
device = st7735(serial)

try:
    #font = ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf', 10)
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
    while True:
        with canvas(device) as draw:
            hostname = socket.gethostname()
            hostip = socket.gethostbyname(hostname)
#*****get data from redis db*****
            temperature = round(float(redis_db.get('Temperature')),1)
            humidity = round(float(redis_db.get('Humidity')),1)
            pressure = round(float(redis_db.get('Pressure')))
            door_sensor_1 = redis_db.get('door_sensor_1')
            door_sensor_2 = redis_db.get('door_sensor_2')
            door_sensor_3 = redis_db.get('door_sensor_3')

#*****draw on lcd********

            draw.line([(0,0),(127,0)], fill = "red",width = 6)
            draw.line([(127,0),(127,127)], fill = "red",width = 3)
            draw.line([(127,127),(0,127)], fill = "red",width = 3)
            draw.line([(0,127),(0,0)], fill = "red",width = 5)

            draw.rectangle([(5,124),(124,6)],fill = "white")

            draw.text((x, top+10),       'IP:', font=font, fill="red")
            draw.text((x+20, top+10),    str(hostip), font=font, fill="blue")

            draw.text((x, top+25),'Temperature.', font=font, fill="red")
            draw.text((x+74, top+25),str(temperature) + 'C', font=font, fill="blue")
            draw.text((x, top+36),'Humidity....',  font=font, fill="red")
            draw.text((x+74, top+36),str(humidity) + '%',  font=font, fill="blue")
            draw.text((x, top+48),'Pressure....',  font=font, fill="red")
            draw.text((x+74, top+48),str(pressure) + 'hPa',  font=font, fill="blue")

            draw.text((x, top+62),'Door 1......',  font=font, fill="red")
            draw.text((x+74, top+62),str(door_sensor_1),  font=font, fill="blue")
            draw.text((x, top+73),'Door 2......',  font=font, fill="red")
            draw.text((x+74, top+73), str(door_sensor_2),  font=font, fill="blue")
            draw.text((x, top+84),'Door 3......',  font=font, fill="red")
            draw.text((x+74, top+84),str(door_sensor_3),  font=font, fill="blue")

except KeyboardInterrupt:
    print("Error")
GPIO.cleanup()
