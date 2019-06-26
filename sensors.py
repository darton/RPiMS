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

from picamera import PiCamera
from gpiozero import LED, Button, MotionSensor
from gpiozero.tools import any_values
from signal import pause
from time import sleep
import subprocess
import redis

#Localization
location = "My Home"

#verbose mode: yes/no
verbose = "yes"

#use zabbix_sender: yes/no
zabbix_sender = "no"

#use picamera: yes/no
use_picamera = "no"

#use door sensor: yes/no
use_door_sensor = "yes"

#use motion sensor: yes/no
use_motion_sensor = "no"

# Led Lamp on GPIO 14
led = LED(14)

#Button type sensors inputs: Door/Window, Smoke Alarm, CO Alarm, CO2 Alarm, Heat Alarm, Water Alarm sensors inputs (store the ref of functions in variable)

button1 = Button(22)
button2 = Button(23)
button3 = Button(16)
button4 = Button(20)
button5 = Button(21)
button6 = Button(5)
button7 = Button(6)
button8 = Button(13)
button9 = Button(19)
button10 = Button(26)

#Motion Sensor inputs:
MotionSensor_1 = MotionSensor(12)

button_sensor_list = {
    "door_sensor_1" : button1,
    "door_sensor_2" : button2,
    "button_1"      : button3,
    "button_2"      : button4,
    "button_3"      : button5,
    "joystick_left" : button6,
    "joystick_up"   : button7,
    "joystick_fire" : button8,
    "joystick_down" : button9,
    "joystick_right": button10
}

motion_sensor_list = {
    "MotionSensor_1": MotionSensor_1,
}

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
redis_db.set("Location", location)

if verbose is "yes" :
    redis_db.set("verbose", '1')
else:
    redis_db.set("verbose", '0')

if zabbix_sender is "yes" :
    redis_db.set("zabbix_sender", '1')
else:
    redis_db.set("zabbix_sender", '0')

if use_picamera is "yes" :
    redis_db.set("use_picamera", '1')
else:
    redis_db.set("use_picamera", '0')

if use_door_sensor is "yes" :
    redis_db.set("use_door_sensor", '1')
else:
    redis_db.set("use_door_sensor", '0')

if use_motion_sensor is "yes" :
    redis_db.set("use_motion_sensor", '1')
else:
    redis_db.set("use_motion_sensor", '0')


# --- Funcions ---

def program_remote_control():
    aaa = redis_db.get('verbose')
    if aaa is '1' :
        verbose = "yes"
    if aaa is '0' :
        verbose = "no"
    return verbose

def door_action_closed(door_id):
    verbose =  program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " has been closed!")

    redis_db.set(str(door_id), 'closed')
    
    if zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_has_been_closed' + " " + str(door_id)
        subprocess.call(zabbix_sender_cmd, shell=True)

    if use_picamera is 'yes':
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh stop", shell=True)
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/videorecorder.sh", shell=True)
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh start", shell=True)

def door_action_opened(door_id):
    verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " has been opened!")
    redis_db.set(str(door_id), 'opened')
    led.source = any_values(sensor1.values, sensor2.values, sensor3.values, sensor4.values )
    if zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_has_been_opened' + " " + str(door_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh stop", shell=True)
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/videorecorder.sh", shell=True)
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh start", shell=True)
        sleep(1)

def door_status_open(door_id):
    verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " is opened!")
    redis_db.set(str(door_id), 'open')
    
    if zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_is_opened' + " " + str(door_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh start", shell=True)

def door_status_close(door_id):
    verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " is closed!")
    redis_db.set(str(door_id), 'close')
    led.source = any_values(sensor1.values, sensor2.values, sensor3.values, sensor4.values )
    if zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_is_closed' + " " + str(door_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh start", shell=True)

def motion_sensor_when_motion(ms_id):
    verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(ms_id) + ": motion was detected")
    redis_db.set(str(ms_id), 'motion')
    if zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_motion' + " " + str(ms_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh start", shell=True)

def motion_sensor_when_no_motion(ms_id):
    verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(ms_id) + ": no motion")
    redis_db.set(str(ms_id), 'nomotion')
    if zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_no_motion' + " " + str(ms_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh start", shell=True)


def sensors_read_once():
    for s in button_sensor_list:
        if button_sensor_list[s].value == 0:
            door_status_open(s)
        else:
            door_status_close(s)

# --- Read sensors when startup ---

sensors_read_once()


# --- Main program ---

if use_door_sensor is 'yes' :
    for s in button_sensor_list:
            button_sensor_list[s].when_pressed = lambda s=s : door_action_closed(s)
            button_sensor_list[s].when_released = lambda s=s : door_action_opened(s)

if use_motion_sensor is 'yes' :
    for s in motion_sensor_list:
            motion_sensor_list[s].when_motion = lambda s=s : motion_sensor_when_motion(s)
            motion_sensor_list[s].when_no_motion = lambda s=s : motion_sensor_when_no_motion(s)
pause()
