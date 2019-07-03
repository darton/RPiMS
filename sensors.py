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
led = LED(18)

#Button type sensors inputs: Door/Window, Smoke Alarm, CO Alarm, CO2 Alarm, Heat Alarm, Water Alarm sensors inputs (store the ref of functions in variable)

door_sensor_1 = Button(27)
door_sensor_2 = Button(22)
door_sensor_3 = Button(23)
button1 = Button(21)
button2 = Button(20)
button3 = Button(16)
joystick_left = Button(5)
joystick_up = Button(6)
joystick_fire = Button(13)
joystick_down = Button(19)
joystick_right = Button(26)

#Motion Sensor inputs:
MotionSensor_1 = MotionSensor(12)

button_sensor_list = {
    "button_1"      : button1,
    "button_2"      : button2,
    "button_3"      : button3,
    "joystick_left" : joystick_left,
    "joystick_up"   : joystick_up,
    "joystick_fire" : joystick_fire,
    "joystick_down" : joystick_down,
    "joystick_right": joystick_right
}

door_sensor_list = {
    "door_sensor_1" : door_sensor_1,
    "door_sensor_2" : door_sensor_2,
    "door_sensor_3" : door_sensor_3
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
    redis_db.set(str(door_id), 'close')
    verbose =  program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " has been closed!")
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
    redis_db.set(str(door_id), 'open')
    led.source = any_values(door_sensor_1.values, door_sensor_2.values, door_sensor_3.values)   
    verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " has been opened!") 
    if zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_has_been_opened' + " " + str(door_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        sleep(0.2)
        av_stream('stop')
        sleep(0.2)
        subprocess.call("/home/pi/scripts/RPiMS/videorecorder.sh", shell=True)
        sleep(0.2)
        av_stream('start')
        sleep(1)

def door_status_open(door_id):
    redis_db.set(str(door_id), 'open')
    verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " is opened!")   
    if zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_is_opened' + " " + str(door_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        av_stream('start')

def door_status_close(door_id):
    redis_db.set(str(door_id), 'close')
    led.source = any_values(door_sensor_1.values, door_sensor_2.values, door_sensor_3.values)
    verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " is closed!")
    if zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_is_closed' + " " + str(door_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        av_stream('start')

def motion_sensor_when_motion(ms_id):
    redis_db.set(str(ms_id), 'motion')
    verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(ms_id) + ": motion was detected")
    if zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_motion' + " " + str(ms_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        av_stream('start')

def motion_sensor_when_no_motion(ms_id):
    redis_db.set(str(ms_id), 'nomotion')
    verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(ms_id) + ": no motion")

def av_stream(state):
    if use_picamera is 'yes':
        subprocess.call("/home/pi/scripts/RPiMS/stream.sh" + " " +  state, shell=True)

# --- Main program ---

if use_door_sensor is 'yes' :
    for s in door_sensor_list:
        if door_sensor_list[s].value == 0:
            door_status_open(s)
        else:
            door_status_close(s)
    for s in door_sensor_list:
            door_sensor_list[s].when_pressed = lambda s=s : door_action_closed(s)
            door_sensor_list[s].when_released = lambda s=s : door_action_opened(s)

if use_motion_sensor is 'yes' :
    for s in motion_sensor_list:
            motion_sensor_list[s].when_motion = lambda s=s : motion_sensor_when_motion(s)
            motion_sensor_list[s].when_no_motion = lambda s=s : motion_sensor_when_no_motion(s)
            
pause()
