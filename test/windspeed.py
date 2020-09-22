#!/usr/bin/env python3

from gpiozero import Button
from signal import pause
from time import sleep, time

interval = 5
pulse = 0
wind_speed_sensor = Button(21,bounce_time=0.05)

def pulse_counter():
    global pulse
    pulse += 1

def reset_pulse_counter():
    global pulse
    pulse = 0

wind_speed_sensor.when_pressed = pulse_counter

while True:
    rotations = pulse/2
    #print(str(rotations) + " per " + str(interval) + " sec")
    wind_speed = round(rotations * 2.4/interval,1)
    print(str(wind_speed) + " km/h")
    reset_pulse_counter()
    sleep(interval)
