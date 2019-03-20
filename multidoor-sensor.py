#!/usr/bin/env python3

from gpiozero import LED, Button
from gpiozero.tools import any_values
from signal import pause
from time import sleep
import subprocess

door1_id = 1
door2_id = 2
door3_id = 3
door4_id = 4

door_sensor1 = Button(22,bounce_time=0.05)
door_sensor2 = Button(23,bounce_time=0.05)
door_sensor3 = Button(24,bounce_time=0.05)
door_sensor4 = Button(25,bounce_time=0.05)

led = LED(14)

door_id = 0

# --- Funcions ---

def door_action_closed(door_id):
    print("The door number " + str(door_id) + " has ben closed!")
    led.source = any_values(door_sensor1.values, door_sensor2.values, door_sensor3.values, door_sensor4.values )
    args ='/home/pi/scripts/zabbix_sender.sh info_when_door_has_been_closed' + " " + str(door_id)
    subprocess.call(args, shell=True)
# Uncomment the lines below if you have PiCamera
#    sleep(0.2)
#    subprocess.call("/home/pi/scripts/stream.sh stop", shell=True)
#    sleep(0.2)
#    subprocess.call("/home/pi/scripts/videorecorder.sh", shell=True)
#    sleep(0.2)
#    subprocess.call("/home/pi/scripts/stream.sh start", shell=True)


def door_action_opened(door_id):
    print("The door number " + str(door_id) + " has ben opened!")
    led.source = any_values(door_sensor1.values, door_sensor2.values, door_sensor3.values, door_sensor4.values )
    args ='/home/pi/scripts/zabbix_sender.sh info_when_door_has_been_opened' + " " + str(door_id)
    subprocess.call(args, shell=True)
# Uncomment the lines below if you have PiCamera
#    sleep(0.2)
#    camera.capture('/home/pi/video/image.jpg')
#    subprocess.call("/home/pi/scripts/stream.sh stop", shell=True)
#    sleep(0.2)
#    subprocess.call("/home/pi/scripts/videorecorder.sh", shell=True)
#    sleep(0.2)
#    subprocess.call("/home/pi/scripts/stream.sh start", shell=True)
#    sleep(1)


def door_status_open(door_id):
    print("The door number " + str(door_id) + " is opened!")
    led.source = any_values(door_sensor1.values, door_sensor2.values, door_sensor3.values, door_sensor4.values )
    args ='/home/pi/scripts/zabbix_sender.sh info_when_door_is_opened' + " " + str(door_id)
    subprocess.call(args, shell=True)
# Uncomment the lines below if you have PiCamera
#    subprocess.call("/home/pi/scripts/stream.sh start", shell=True)


def door_status_close(door_id):
    print("The door number " + str(door_id) + " is closed!")
    led.source = any_values(door_sensor1.values, door_sensor2.values, door_sensor3.values, door_sensor4.values )
    args ='/home/pi/scripts/zabbix_sender.sh info_when_door_is_closed' + " " + str(door_id)
    subprocess.call(args, shell=True)
# Uncomment the lines below if you have PiCamera
#    subprocess.call("/home/pi/scripts/stream.sh start", shell=True)


# --- Test sensors when startup ---

if door_sensor1.value == 0:
    door_status_open(door1_id)
else:
    door_status_close(door1_id)


if door_sensor2.value == 0:
    door_status_open(door2_id)
else:
    door_status_close(door2_id)


if door_sensor3.value == 0:
    door_status_open(door3_id)
else:
    door_status_close(door3_id)


if door_sensor4.value == 0:
    door_status_open(door4_id)
else:
    door_status_close(door4_id)


# --- Main program ---

door_sensor1.when_pressed = lambda : door_action_closed(door1_id)
door_sensor1.when_released = lambda : door_action_opened(door1_id)

door_sensor2.when_pressed = lambda : door_action_closed(door2_id)
door_sensor2.when_released = lambda : door_action_opened(door2_id)

door_sensor3.when_pressed = lambda : door_action_closed(door3_id)
door_sensor3.when_released = lambda : door_action_opened(door3_id)

door_sensor4.when_pressed = lambda : door_action_closed(door4_id)
door_sensor4.when_released = lambda : door_action_opened(door4_id)

pause()
