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
x = 0

serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 25, gpio_RST = 27)

device = st7735(serial)

device = st7735(serial, width=128, height=128, h_offset=1, v_offset=2, bgr=True, persist=False )

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
            CPUtemperature = round(float(redis_db.get('CPUtemperature')),1)

#*****draw on lcd********
#            draw.line([(0,0),(127,0)], fill = "blue",width = 6)
#            draw.line([(127,0),(127,127)], fill = "blue",width = 3)
#            draw.line([(127,127),(0,127)], fill = "blue",width = 3)
#            draw.line([(0,127),(0,0)], fill = "blue",width = 5)
#            draw.rectangle(device.bounding_box, outline="white", fill="black")

#            draw.rectangle([(5,124),(124,6)], outline="red", fill="black")

            draw.text((x, top+12),       ' IP', font=font, fill="yellow")
            draw.text((x+17, top+12),'', font=font, fill="blue")
            draw.text((x+22, top+12),    str(hostip), font=font, fill="white")

            draw.text((x, top+25),' Temperature', font=font, fill="red")
            draw.text((x+71, top+25),'', font=font, fill="blue")
            draw.text((x+77, top+25),str(temperature) + '*C', font=font, fill="white")

            draw.text((x, top+38),' Humidity',  font=font, fill="blue")
            draw.text((x+70, top+38),'', font=font, fill="blue")
            draw.text((x+77, top+38),str(humidity) + '%',  font=font, fill="white")
            
            draw.text((x, top+51),' Pressure',  font=font, fill="green")
            draw.text((x+70, top+51),'', font=font, fill="blue")
            draw.text((x+77, top+51),str(pressure) + 'hPa',  font=font, fill="white")

            draw.text((x, top+64),' Door 1',  font=font, fill="yellow")
            draw.text((x+70, top+64),'', font=font, fill="blue")
            draw.text((x+77, top+64),str(door_sensor_1),  font=font, fill="white")
            
            draw.text((x, top+77),' Door 2',  font=font, fill="yellow")
            draw.text((x+70, top+77),'', font=font, fill="blue")
            draw.text((x+77, top+77), str(door_sensor_2),  font=font, fill="white")
            
            draw.text((x, top+90),' CPU temp',  font=font, fill="red")
            draw.text((x+77, top+90),str(CPUtemperature)+ "*C",  font=font, fill="white")

except KeyboardInterrupt:
    print("The End")
    GPIO.cleanup()
