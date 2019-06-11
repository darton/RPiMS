#!/usr/bin/env python3

#
#  Author : Dariusz Kowalczyk
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License Version 2 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#from picamera import PiCamera
from gpiozero import LED, Button
from gpiozero.tools import any_values
from signal import pause
from time import sleep
import subprocess
import redis

# picamera yes/no
picamera = "no"

# Led Lamp on GPIO 14
led = LED(14)

#Motion Sensor on GPIO 27
pir = MotionSensor(27)

# Door sensors inputs (store the ref of functions in variable)
sensor1 = Button(22,bounce_time=0.05)
sensor2 = Button(23,bounce_time=0.05)
sensor3 = Button(24,bounce_time=0.05)
sensor4 = Button(25,bounce_time=0.05)

active_sensor_list = {
    "door_sensor_1": sensor1,
    "door_sensor_2": sensor2,
    "door_sensor_3": sensor3,
    "door_sensor_4": sensor4
}


redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

redis_db.set("Location", 'Serwerownia Z2')


# --- Funcions ---

def door_action_closed(door_id):
    print("The " + str(door_id) + " has been closed!")
    redis_db.set(str(door_id), 'closed')
    led.source = any_values(sensor1.values, sensor2.values, sensor3.values, sensor4.values )
    zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_has_been_closed' + " " + str(door_id)
    subprocess.call(zabbix_sender_cmd, shell=True)

    if picamera is 'yes':
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh stop", shell=True)
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/videorecorder.sh", shell=True)
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh start", shell=True)

def door_action_opened(door_id):
    print("The " + str(door_id) + " has been opened!")
    redis_db.set(str(door_id), 'opened')
    led.source = any_values(sensor1.values, sensor2.values, sensor3.values, sensor4.values )
    zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_has_been_opened' + " " + str(door_id)
    subprocess.call(zabbix_sender_cmd, shell=True)
    if picamera is 'yes':
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh stop", shell=True)
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/videorecorder.sh", shell=True)
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh start", shell=True)
        sleep(1)

def door_status_open(door_id):
    print("The " + str(door_id) + " is opened!")
    redis_db.set(str(door_id), 'open')
    led.source = any_values(sensor1.values, sensor2.values, sensor3.values, sensor4.values )
    zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_is_opened' + " " + str(door_id)
    subprocess.call(zabbix_sender_cmd, shell=True)
    if picamera is 'yes':
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh start", shell=True)


def door_status_close(door_id):
    print("The " + str(door_id) + " is closed!")
    redis_db.set(str(door_id), 'close')
    led.source = any_values(sensor1.values, sensor2.values, sensor3.values, sensor4.values )
    zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_is_closed' + " " + str(door_id)
    subprocess.call(zabbix_sender_cmd, shell=True)
    if picamera is 'yes':
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh start", shell=True)

def sensors_read_once():
    for s in active_sensor_list:
        if active_sensor_list[s].value == 0:
            door_status_open(s)
        else:
            door_status_close(s)
        active_sensor_list[s].when_pressed = lambda : door_action_closed(s)
        active_sensor_list[s].when_released = lambda : door_action_opened(s)

# --- Read sensors when startup ---
sensors_read_once()

# --- Main program ---

#for s in active_sensor_list:
#        active_sensor_list[s].when_pressed = lambda : door_action_closed(s)
#        active_sensor_list[s].when_released = lambda : door_action_opened(s)

sensor1.when_pressed = lambda : door_action_closed("sensor1")
sensor1.when_released = lambda : door_action_opened("sensor1")

sensor2.when_pressed = lambda : door_action_closed("sensor2")
sensor2.when_released = lambda : door_action_opened("sensor2")

sensor3.when_pressed = lambda : door_action_closed("sensor3")
sensor3.when_released = lambda : door_action_opened("sensor3")

sensor4.when_pressed = lambda : door_action_closed("sensor4")
sensor4.when_released = lambda : door_action_opened("sensor4")

pir.when_motion = lambda : print("motion yes")
pir.when_no_motion = lambda : print("motion no")

pause()
