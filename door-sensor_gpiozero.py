#!/usr/bin/env python

from gpiozero import LED, Button
from signal import pause
from time import sleep

button = Button(27,bounce_time=0.1)
led = LED(14)

def door_action_closed():
    print("The door has been closed!")
    led.source = button.values

def door_action_opened():
    print("The door has been opened!")
    led.source = button.values

def door_status_open():
    print("The door is opened!")
    led.source = button.values

def door_status_close():
    print("The door is closed!")
    led.source = button.values

if button.value == 0:
    door_status_open()
else:
    door_status_close()

button.when_pressed = door_action_closed
button.when_released = door_action_opened

pause()
