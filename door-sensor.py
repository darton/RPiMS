#!/usr/bin/env python

from gpiozero import LED, Button
from signal import pause
from time import sleep

button = Button(27)
led = LED(14)

def door_closed():
    print("The door has ben closed!")
    sleep(0.1)

def door_opened():
    print("The door has ben opened!")
    led.source = button.values
    sleep(0.1)

button.when_pressed = door_closed
button.when_released = door_opened

pause()
