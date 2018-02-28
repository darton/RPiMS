#!/usr/bin/env python

#from picamera import PiCamera
from gpiozero import LED, Button
from signal import pause
from time import sleep
import subprocess

button = Button(27,bounce_time=0.1)
led = LED(14)
#camera = PiCamera()

led.source = button.values

def door_action_closed():
    print("The door has ben closed!")
    led.source = button.values
    subprocess.call("/home/pi/scripts/zabbix_sender.sh info_when_door_has_been_closed", shell=True)
    sleep(0.2)
    subprocess.call("/home/pi/scripts/stream.sh stop", shell=True)


def door_action_opened():

    print("The door has ben opened!")
    led.source = button.values
    subprocess.call("/home/pi/scripts/zabbix_sender.sh info_when_door_has_been_opened", shell=True)
    sleep(0.2)
#    camera.capture('/home/pi/video/image.jpg')
    subprocess.call("/home/pi/scripts/videorecorder.sh", shell=True)
    sleep(1)
    subprocess.call("/home/pi/scripts/stream.sh start", shell=True)
    sleep(1)


def door_status_open():
    print("The door is opened!")
    subprocess.call("/home/pi/scripts/zabbix_sender.sh info_when_door_is_opened", shell=True)


def door_status_close():
    print("The door is closed!")
    subprocess.call("/home/pi/scripts/zabbix_sender.sh info_when_door_is_closed", shell=True)



if button.value == 0:
    door_status_open()
else:
    door_status_close()

button.when_pressed = door_action_closed
button.when_released = door_action_opened

pause()
