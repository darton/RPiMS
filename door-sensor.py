#!/usr/bin/env python

#from picamera import PiCamera
from gpiozero import LED, Button
from signal import pause
from time import sleep
import subprocess

button = Button(27,bounce_time=0.1)
led = LED(14)
#camera = PiCamera()

def door_action_closed():
    print("The door has ben closed!")
    led.source = button.values
    subprocess.call("/home/pi/scripts/zabbix_sender.sh info_when_door_has_been_closed", shell=True)
    sleep(0.2)

def door_action_opened():
    print("The door has ben opened!")
    led.source = button.values
#    camera.start_preview()
#    button.wait_for_press()
#    sleep(3)
#    camera.capture('/home/pi/video/image.jpg')
#    camera.stop_preview()
    subprocess.call("/home/pi/scripts/zabbix_sender.sh info_when_door_has_been_opened", shell=True)
    sleep(0.2)


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
