#!/usr/bin/env python3

from gpiozero import Button
from signal import pause
from time import sleep, time

bucket_counter = 0
interval = 10

BUCKET_SIZE = 0.2794

def bucket_tipped():
    global bucket_counter
    bucket_counter += 1

def reset_rainfall():
    global bucket_counter
    bucket_counter = 0

rain_sensor = Button(21, hold_time=0.1)
rain_sensor.when_pressed = bucket_tipped

while True:
    rainfall = bucket_counter * BUCKET_SIZE
    print(rainfall,bucket_counter)
    reset_rainfall()
    sleep(interval)
