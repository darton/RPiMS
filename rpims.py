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

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

yes = 1
no = 0

config = {
    #Localization
    "location"               : "My Home",
    #real time control mode: yes/no
    "real_time_control"      : yes,
    #verbose mode: yes/no
    "verbose"                : yes,
    #use zabbix sender: yes/no
    "use_zabbix_sender"      : no,
    #use picamera: yes/no
    "use_picamera"          : yes,
    #recording 5s video on local drive: yes/no
    "use_picamera_recording" : no,
    #use door sensor: yes/no
    "use_door_sensor"        : yes,
    #use motion sensor: yes/no
    "use_motion_sensor"      : yes,
    #use LED indicator: yes/no
    "use_led_indicator"      : yes,
    #use Waveshare display LCD/OLED HAT buttons and joystick
    "use_system_buttons"   : no,
    #use BME280 sensor: yes/no
    "use_BME280_sensor"      : no,
    #use DHT22 sensor: yes/no
    "use_DHT22_sensor"       : no,
    #use DS18B20 sensors: yes/no
    "use_DS18B20_sensor"     : no,
    #Led indicators or relays type outputs
    "door_led_pin"           : 12,
    "motion_led_pin"         : 16,
    # Button type inputs
    "button_1_pin"        : 22,
    "button_1_hold_time"  : 3,
    "button_2_pin"        : 23,
    "button_2_hold_time"  : 3,
    "button_3_pin"        : 13,
    "button_3_hold_time"  : 5,
    # Motion Sensor type inputs
    "motion_sensor_1_pin" : 18,
    "motion_sensor_2_pin" : 20,
    "motion_sensor_3_pin" : 21,
    "motion_sensor_4_pin" : 26,
    "motion_sensor_5_pin" : 19,
    "motion_sensor_6_pin" : 5,
    "motion_sensor_7_pin" : 6,
}


for s in config :
    print(s + ' = ' + str(config[s]))
    redis_db.set(s, config[s])

if config['use_door_sensor'] is yes :
    door_sensor_list = {
        "door_sensor_1" : Button(config['button_1_pin'], hold_time=config['button_1_hold_time']),
        "door_sensor_2" : Button(config['button_2_pin'], hold_time=config['button_2_hold_time']),
    }

if config['use_motion_sensor'] is yes :
    motion_sensor_list = {
        "motion_sensor_1": MotionSensor(config['motion_sensor_1_pin']),
        "motion_sensor_2": MotionSensor(config['motion_sensor_2_pin']),
        "motion_sensor_3": MotionSensor(config['motion_sensor_3_pin']),
        "motion_sensor_4": MotionSensor(config['motion_sensor_4_pin']),
        "motion_sensor_5": MotionSensor(config['motion_sensor_5_pin']),
        "motion_sensor_6": MotionSensor(config['motion_sensor_6_pin']),
        "motion_sensor_7": MotionSensor(config['motion_sensor_7_pin']),
    }

if config['use_system_buttons'] is "yes" :
    system_buttons = {
        "shutdown_button" : Button(config['button_3_pin'], hold_time=config['button_3_thold_time']),
    }

if config['use_led_indicator'] is yes :
    led_list = {
        "door_led" : LED(config['door_led_pin']),
        "motion_led" : LED(config['motion_led_pin']),
    }


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
    if config['real_time_control'] is yes:
        verbose =  program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " has been closed!")
    if config['use_zabbix_sender'] is yes :
        zabbix_sender_call('info_when_door_has_been_closed',door_id)
    if config['use_picamera'] is yes:
         if detect_no_alarms():
             av_stream('stop')


def door_action_opened(door_id):
    redis_db.set(str(door_id), 'open')
    if config['real_time_control'] is yes:
        verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " has been opened!")
    if config['use_zabbix_sender'] is yes :
        zabbix_sender_call('info_when_door_has_been_opened',door_id)
    if config['use_picamera'] is yes :
        if config['use_picamera_recording'] is 'yes':
            av_stream('stop')
            subprocess.call("/home/pi/scripts/RPiMS/videorecorder.sh", shell=True)
        av_stream('start')


def door_status_open(door_id):
    redis_db.set(str(door_id), 'open')
    if config['real_time_control'] is yes:
        verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " is opened!")
    if config['use_zabbix_sender'] is yes:
        zabbix_sender_call('info_when_door_is_opened',door_id)
    if config['use_picamera'] is yes:
        av_stream('start')


def door_status_close(door_id):
    redis_db.set(str(door_id), 'close')
    if config['real_time_control'] is yes:
        verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(door_id) + " is closed!")
    if config['use_zabbix_sender'] is yes :
        zabbix_sender_call('info_when_door_is_closed',door_id)
    if config['use_picamera'] is yes:
         if detect_no_alarms():
             av_stream('stop')


def motion_sensor_when_motion(ms_id):
    redis_db.set(str(ms_id), 'motion')
    if config['real_time_control'] is yes:
        verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(ms_id) + ": motion was detected")
    if config['use_zabbix_sender'] is yes :
        zabbix_sender_call('info_when_motion',ms_id)
    if config['use_picamera'] is yes:
        av_stream('start')


def motion_sensor_when_no_motion(ms_id):
    redis_db.set(str(ms_id), 'nomotion')
    if config['real_time_control'] is yes:
        verbose = program_remote_control()
    if verbose is 'yes' :
        print("The " + str(ms_id) + ": no motion")
    if config['use_picamera'] is yes:
         if detect_no_alarms():
             av_stream('stop')


def detect_no_alarms():
    if config['use_door_sensor'] is yes and config['use_motion_sensor'] is yes:
        door_sensor_values = []
        motion_sensor_values = []
        for s in door_sensor_list:
            door_sensor_values.append(door_sensor_list[s].value)
        for s in motion_sensor_list:
            motion_sensor_values.append(int(not motion_sensor_list[s].value))
        if all(door_sensor_values) and all(motion_sensor_values):
            return True
    if config['use_door_sensor'] is yes and config['use_motion_sensor'] is no:
        door_sensor_values = []
        for s in door_sensor_list:
            door_sensor_values.append(door_sensor_list[s].value)
        if all(door_sensor_values):
            return True
    if config['use_door_sensor'] is no and config['use_motion_sensor'] is yes:
        motion_sensor_values = []
        for s in motion_sensor_list:
            motion_sensor_values.append(int(not motion_sensor_list[s].value))
        if all(motion_sensor_values):
            return True


def av_stream(state):
    subprocess.call("/home/pi/scripts/RPiMS/stream.sh" + " " +  state, shell=True)


def zabbix_sender_call(message,sensor_id):
    zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh ' + message + " " + str(sensor_id)
    subprocess.call(zabbix_sender_cmd, shell=True)


def shutdown():
    check_call(['sudo', 'poweroff'])


# --- Main program ---
print('# RPiMS is running #')
print('')

if config['use_door_sensor'] is yes :
    for s in door_sensor_list:
        if door_sensor_list[s].value == 0:
            door_status_open(s)
        else:
            door_status_close(s)
    for s in door_sensor_list:
            door_sensor_list[s].when_held = lambda s=s : door_action_closed(s)
            door_sensor_list[s].when_released = lambda s=s : door_action_opened(s)
    if config['use_led_indicator'] is yes :
        led_list['door_led'].source = all_values(*door_sensor_list.values())

if config['use_motion_sensor'] is yes :
    for s in motion_sensor_list:
            motion_sensor_list[s].when_motion = lambda s=s : motion_sensor_when_motion(s)
            motion_sensor_list[s].when_no_motion = lambda s=s : motion_sensor_when_no_motion(s)
    if config['use_led_indicator'] is yes :
        led_list['motion_led'].source = any_values(*motion_sensor_list.values())

if config['use_system_buttons'] is yes :
    system_buttons['shutdown_button'].when_held = shutdown

pause()
