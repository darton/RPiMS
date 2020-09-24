#!/usr/bin/env python3

import statistics
import redis
from gpiozero import Button
from signal import pause
from time import sleep, time

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

wind_speed_acquisition_time = 6
wind_speed_agregation_time = 3600
wind_speed_sensor_pulse = 0
wind_speeds = []
pulse = 0

def pulse_counter():
    global pulse
    pulse += 1

def reset_pulse_counter():
    global pulse
    pulse = 0

def calculate_speed(wind_speed_acquisition_time):
    global pulse
    rotations = pulse/2
    wind_speed_km_per_hour = round(rotations * 2.4/wind_speed_acquisition_time,1)
    return wind_speed_km_per_hour

wind_speed_sensor = Button(21)
wind_speed_sensor.when_pressed = pulse_counter

while True:
    start_time = time()
    while time() - start_time <= wind_speed_acquisition_time:
        reset_pulse_counter()
        sleep(wind_speed_acquisition_time)
        wind_speed = calculate_speed(wind_speed_acquisition_time)
        if len(wind_speeds) == (wind_speed_agregation_time/wind_speed_acquisition_time + 1):
            del wind_speeds[0]
        wind_speeds.append(wind_speed)
    wind_gust = max(wind_speeds)
    wind_mean_speed = round(statistics.mean(wind_speeds),1)
    print("Wind mean speed: " + str(wind_mean_speed) + " km/h", " Wind gust: " + str(wind_gust) + "km/h","Wind speed " + str(wind_speed) + " km/h" )
    redis_db.mset({'wind_mean_speed' : wind_mean_speed,'wind_gust' : wind_gust, 'wind_speed' : wind_speed})
