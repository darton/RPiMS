#!/usr/bin/env python3

import redis
import math
from gpiozero import Button
from signal import pause
from time import sleep, time

bucket_counter = 0
rainfall_acquisition_time = 6
rainfalls = []

BUCKET_SIZE = 0.2794 #[mm]

def bucket_tipped():
    global bucket_counter
    bucket_counter += 1

def reset_bucket_counter():
    global bucket_counter
    bucket_counter = 0

def calculate_rainfall():
    rainfall = round(bucket_counter * BUCKET_SIZE,0)
    return rainfall


redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
rain_sensor = Button(21, hold_time=0.1)
rain_sensor.when_pressed = bucket_tipped

while True:
    start_time = time()
    while time() - start_time <= rainfall_acquisition_time:
        reset_bucket_counter()
        sleep(rainfall_acquisition_time)
        rainfall = calculate_rainfall()
        if len(rainfalls) == (3600*24/rainfall_acquisition_time + 1):
            rainfalls.clear()
        rainfalls.append(rainfall)
    daily_rainfall = round(math.fsum(rainfalls),1)
    print("Rainfall: " + str(rainfall) + " mm ", "Daily rainfall: " + str(daily_rainfall) + " mm")
    redis_db.mset({'daily_rainfall': daily_rainfall,'rainfall': rainfall})
