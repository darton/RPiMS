#!/usr/bin/env python3

# -*- coding:utf-8 -*-
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
from gpiozero.tools import all_values, any_values
from subprocess import check_call
from signal import pause
#from time import sleep
import subprocess
import redis

#Localization
location = "My Home"

#real time control mode: yes/no
real_time_control = "yes"

#verbose mode: yes/no
verbose = "yes"

#use zabbix sender: yes/no
use_zabbix_sender = "no"

#use picamera: yes/no
use_picamera = "no"

#recording 5s video on local drive: yes/no
use_picamera_recording = "no"

#use door sensor: yes/no
use_door_sensor = "yes"

#use motion sensor: yes/no
use_motion_sensor = "no"

#use LED indicator: yes/no
use_led_indicator = "yes"

#use Waveshare display LCD/OLED HAT buttons and joystick
use_hat_buttons = "no"

#use BME280 sensor: yes/no
use_BME280_sensor = "no"

#use DHT22 sensor: yes/no
use_DHT22_sensor = "no"

#use DS18B20 sensor: yes/no
use_DS18B20_sensor = "no"


## GPIO outputs
# Led indicators or Relays
led_list = {
    "door_led" : LED(14),
    "motion_led" : LED(15),
}

## GPIO inputs
#Button type sensors inputs like: Door/Window, Smoke Alarm, CO Alarm, CO2 Alarm, Heat Alarm, Water Alarm
door_sensor_list = {
    "door_sensor_1" : Button(22, hold_time=3),
    "door_sensor_2" : Button(23, hold_time=3),
}

#Motion Sensor inputs
motion_sensor_list = {
    "motion_sensor_1": MotionSensor(18),
    "motion_sensor_2": MotionSensor(12),
}

#Waveshare display Hat (LCD/OLED) with buttons and joystick
hat_button_list = {
    "button_1"      : Button(21),
    "button_2"      : Button(20),
    "button_3"      : Button(16),
    "joystick_left" : Button(5),
    "joystick_up"   : Button(6),
    "joystick_fire" : Button(13, hold_time=5),
    "joystick_down" : Button(19),
    "joystick_right": Button(26)
}

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
redis_db.set("Location", location)

if verbose is "yes" :
    redis_db.set("verbose", '1')
else:
    redis_db.set("verbose", '0')

if use_zabbix_sender is "yes" :
    redis_db.set("use_zabbix_sender", '1')
else:
    redis_db.set("use_zabbix_sender", '0')

if use_picamera is "yes" :
    redis_db.set("use_picamera", '1')
else:
    redis_db.set("use_picamera", '0')

if use_picamera_recording is "yes" :
    redis_db.set("use_picamera_recording", '1')
else:
    redis_db.set("use_picamera_recording", '0')

if use_door_sensor is "yes" :
    redis_db.set("use_door_sensor", '1')
else:
    redis_db.set("use_door_sensor", '0')

if use_motion_sensor is "yes" :
    redis_db.set("use_motion_sensor", '1')
else:
    redis_db.set("use_motion_sensor", '0')

if use_led_indicator is "yes" :
    redis_db.set("use_led_indicator", '1')
else:
    redis_db.set("use_led_indicator", '0')

if use_hat_buttons is "yes" :
    redis_db.set("use_hat_buttons", '1')
else:
    redis_db.set("use_hat_buttons", '0')

if use_BME280_sensor is "yes" :
    redis_db.set("use_BME280_sensor", '1')
else:
    redis_db.set("use_BME280_sensor", '0')

if use_DHT22_sensor is "yes" :
    redis_db.set("use_DHT22_sensor", '1')
else:
    redis_db.set("use_DHT22_sensor", '0')

if use_DS18B20_sensor is "yes" :
    redis_db.set("use_DS18B20_sensor", '1')
else:
    redis_db.set("use_DS18B20_sensor", '0')

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
    if real_time_control is 'yes':
        verbose =  program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " has been closed!")
    if use_zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_has_been_closed' + " " + str(door_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
         if detect_no_alarms():
             av_stream('stop')

def door_action_opened(door_id):
    redis_db.set(str(door_id), 'open')
    if real_time_control is 'yes':
        verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " has been opened!")
    if use_zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_has_been_opened' + " " + str(door_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        if use_picamera_recording is 'yes':
            av_stream('stop')
            subprocess.call("/home/pi/scripts/RPiMS/videorecorder.sh", shell=True)
        av_stream('start')

def door_status_open(door_id):
    redis_db.set(str(door_id), 'open')
    if real_time_control is 'yes':
        verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " is opened!")
    if use_zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_is_opened' + " " + str(door_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        av_stream('start')

def door_status_close(door_id):
    redis_db.set(str(door_id), 'close')
    if real_time_control is 'yes':
        verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " is closed!")
    if use_zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_door_is_closed' + " " + str(door_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
         if detect_no_alarms():
             av_stream('stop')

def motion_sensor_when_motion(ms_id):
    redis_db.set(str(ms_id), 'motion')
    if real_time_control is 'yes':
        verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(ms_id) + ": motion was detected")
    if use_zabbix_sender is 'yes' :
        zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh info_when_motion' + " " + str(ms_id)
        subprocess.call(zabbix_sender_cmd, shell=True)
    if use_picamera is 'yes':
        av_stream('start')

def motion_sensor_when_no_motion(ms_id):
    redis_db.set(str(ms_id), 'nomotion')
    if real_time_control is 'yes':
        verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(ms_id) + ": no motion")
    if use_picamera is 'yes':
         if detect_no_alarms():
             av_stream('stop')

def detect_no_alarms():
    if use_door_sensor is 'yes' and use_motion_sensor is 'yes':
        door_sensor_values = []
        motion_sensor_values = []
        for s in door_sensor_list:
            door_sensor_values.append(door_sensor_list[s].value)
        for s in motion_sensor_list:
            motion_sensor_values.append(int(not motion_sensor_list[s].value))
        if all(door_sensor_values) and all(motion_sensor_values):
            return True
    if use_door_sensor is 'yes' and use_motion_sensor is 'no':
        door_sensor_values = []
        for s in door_sensor_list:
            door_sensor_values.append(door_sensor_list[s].value)
        if all(door_sensor_values):
            return True
    if use_door_sensor is 'no' and use_motion_sensor is 'yes':
        motion_sensor_values = []
        for s in motion_sensor_list:
            motion_sensor_values.append(int(not motion_sensor_list[s].value))
        if all(motion_sensor_values):
            return True

def av_stream(state):
    subprocess.call("/home/pi/scripts/RPiMS/stream.sh" + " " +  state, shell=True)

def shutdown():
    check_call(['sudo', 'poweroff'])


# --- Main program ---
print('# RPiMS is running #')
print('')

if use_door_sensor is 'yes' :
    for s in door_sensor_list:
        if door_sensor_list[s].value == 0:
            door_status_open(s)
        else:
            door_status_close(s)
    for s in door_sensor_list:
            door_sensor_list[s].when_held = lambda s=s : door_action_closed(s)
            door_sensor_list[s].when_released = lambda s=s : door_action_opened(s)
    if use_led_indicator is 'yes' :
        led_list['door_led'].source = all_values(*door_sensor_list.values())

if use_motion_sensor is 'yes' :
    for s in motion_sensor_list:
            motion_sensor_list[s].when_motion = lambda s=s : motion_sensor_when_motion(s)
            motion_sensor_list[s].when_no_motion = lambda s=s : motion_sensor_when_no_motion(s)
    if use_led_indicator is 'yes' :
        led_list['motion_led'].source = any_values(*motion_sensor_list.values())

if use_hat_buttons is "yes" :
    hat_button_list['joystick_fire'].when_held = shutdown

pause()
