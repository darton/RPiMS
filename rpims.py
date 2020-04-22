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
from time import sleep
import threading
import subprocess
import redis
import smbus2
import logging
import sys


redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
yes = 1
no = 0

config = {
    #Localization
    "location"               : "My Home",
    #verbose mode: yes/no
    "verbose"                : yes,
    #use zabbix sender: yes/no
    "use_zabbix_sender"      : no,
    #use picamera: yes/no
    "use_picamera"           : no,
    #recording 5s video on local drive: yes/no
    "use_picamera_recording" : no,
    #use door sensor: yes/no
    "use_door_sensor"        : yes,
    #use motion sensor: yes/no
    "use_motion_sensor"      : yes,
    #use LED indicator: yes/no
    "use_led_indicator"      : no,
    #use system buttons
    "use_system_buttons"     : yes,
    #use serial display
    "use_serial_display"     : yes,
    #serial display type oled_sh1106 or lcd_st7735
    "serial_display_type"    : "lcd_st7735",
    #disaplay refresh rate : in Hz
    "display_refresh_rate"   : 10,
    #use CPU sensor: yes/no
    "use_CPU_sensor"         : yes,
    #CPUtemp read interval : in seconds:
    "CPUtemp_read_interval"  : 1,
    #use BME280 sensor: yes/no
    "use_BME280_sensor"      : yes,
    #BME280 read interval : in seconds:
    "BME280_read_interval"   : 10,
    #use DHT22 sensor: yes/no
    "use_DHT22_sensor"       : no,
    #DHT22 read interval : in seconds:
    "DHT_read_interval"      : 60,
    #use DS18B20 sensors: yes/no
    "use_DS18B20_sensor"     : no,
    #DS18B20 read interval : in seconds:
    "DS18B20_read_interval"  : 60,
    #Led indicators or relays type outputs
    "door_led_pin"           : 22,
    "motion_led_pin"         : 17,
    # Button type inputs
    "button_1_pin"           : 21,
    "button_1_hold_time"     : 1,
    "button_2_pin"           : 20,
    "button_2_hold_time"     : 1,
    "button_3_pin"           : 16,
    "button_3_hold_time"     : 5,
    # Motion Sensor type inputs
    "motion_sensor_1_pin"    : 6,
    "motion_sensor_2_pin"    : 19,
    "motion_sensor_3_pin"    : 5,
    "motion_sensor_4_pin"    : 26,
    "motion_sensor_5_pin"    : 13,
}


logging.basicConfig(filename='/tmp/rpims.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

try:
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
        }

    if config['use_system_buttons'] is yes :
        system_buttons = {
            "shutdown_button" : Button(config['button_3_pin'], hold_time=config['button_3_hold_time']),
        }

    if config['use_led_indicator'] is yes :
        led_list = {
            "door_led" : LED(config['door_led_pin']),
            "motion_led" : LED(config['motion_led_pin']),
        }

except Exception as err :
    logger.error(err)
    print('Problem with ' + str(err))
    sys.exit(1)


# --- Funcions ---

def door_action_closed(door_id):
    redis_db.set(str(door_id), 'close')
    if config['verbose'] is yes :
        print("The " + str(door_id) + " has been closed!")
    if config['use_zabbix_sender'] is yes :
        zabbix_sender_call('info_when_door_has_been_closed',door_id)
    if config['use_picamera'] is yes:
         if detect_no_alarms():
             av_stream('stop')


def door_action_opened(door_id):
    redis_db.set(str(door_id), 'open')
    if config['verbose'] is yes :
        print("The " + str(door_id) + " has been opened!")
    if config['use_zabbix_sender'] is yes :
        zabbix_sender_call('info_when_door_has_been_opened',door_id)
    if config['use_picamera'] is yes :
        if config['use_picamera_recording'] is 'yes':
            av_stream('stop')
            av_recording()
        av_stream('start')


def door_status_open(door_id):
    redis_db.set(str(door_id), 'open')
    if config['verbose'] is yes :
        print("The " + str(door_id) + " is opened!")
    if config['use_zabbix_sender'] is yes:
        zabbix_sender_call('info_when_door_is_opened',door_id)
    if config['use_picamera'] is yes:
        av_stream('start')


def door_status_close(door_id):
    redis_db.set(str(door_id), 'close')
    if config['verbose'] is yes :
        print("The " + str(door_id) + " is closed!")
    if config['use_zabbix_sender'] is yes :
        zabbix_sender_call('info_when_door_is_closed',door_id)
    if config['use_picamera'] is yes:
         if detect_no_alarms():
             av_stream('stop')


def motion_sensor_when_motion(ms_id):
    redis_db.set(str(ms_id), 'motion')
    if config['verbose'] is yes :
        print("The " + str(ms_id) + ": motion was detected")
    if config['use_zabbix_sender'] is yes :
        zabbix_sender_call('info_when_motion',ms_id)
    if config['use_picamera'] is yes:
        av_stream('start')


def motion_sensor_when_no_motion(ms_id):
    redis_db.set(str(ms_id), 'nomotion')
    if config['verbose'] is yes :
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
    subprocess.call("/home/pi/scripts/RPiMS/videostreamer.sh" + " " +  state, shell=True)


def av_recording():
    subprocess.call("/home/pi/scripts/RPiMS/videorecorder.sh", shell=True)


def zabbix_sender_call(message,sensor_id):
    zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh ' + message + " " + str(sensor_id)
    subprocess.call(zabbix_sender_cmd, shell=True)


def shutdown():
    check_call(['sudo', 'poweroff'])


def get_cputemp_data():
    try:
        from gpiozero import CPUTemperature
        while True :
            data = CPUTemperature()
            redis_db.set('CPU_Temperature', data.temperature)
            if config['verbose'] is yes :
                print('CPU temperature: {0:0.1f}'.format(data.temperature),chr(176)+'C', sep='')
            sleep(config['CPUtemp_read_interval'])
    except Exception as err :
        logger.error(err)
        print('Problem with ' + str(err))


def get_bme280_data():
    try:
        import bme280
        port = 1
        address = 0x76
        bus = smbus2.SMBus(port)
        while True :
            calibration_params = bme280.load_calibration_params(bus, address)
            data = bme280.sample(bus, address, calibration_params)
            redis_db.mset({'BME280_Humidity' : data.humidity,'BME280_Temperature' : data.temperature, 'BME280_Pressure' : data.pressure})
            if config['verbose'] is yes :
                print('')
                print('Humidity: {0:0.0f}%'.format(data.humidity))
                print('Temperature: {0:0.1f}\xb0C'.format(data.temperature))
                print('Pressure: {0:0.0f}hPa'.format(data.pressure))
            sleep(config['BME280_read_interval'])
    except Exception as err :
        logger.error(err)
        print('Problem with ' + str(err))


def get_ds18b20_data():
    try:
        from w1thermsensor import W1ThermSensor
        while True :
            data = W1ThermSensor.get_available_sensors([W1ThermSensor.THERM_SENSOR_DS18S20,W1ThermSensor.THERM_SENSOR_DS18S20])
            for sensor in data:
                redis_db.set('DS18B20-' + sensor.id, sensor.get_temperature())
                if config['verbose'] is yes :
                    print("Sensor %s temperature %.2f"%(sensor.id,sensor.get_temperature()),"\xb0C")
            sleep(config['DS18B20_read_interval'])
    except Exception as err :
        logger.error(err)
        print('Problem with ' + str(err))


def oled_sh1106():
    from luma.core.interface.serial import i2c, noop
    from luma.core.render import canvas
    from luma.core import lib
    from luma.oled.device import sh1106
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    import time
    import socket

    # Load default font.
    font = ImageFont.load_default()
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = 128
    height = 64
    image = Image.new('1', (width, height))
    # First define some constants to allow easy resizing of shapes.
    padding = 0
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    serial = i2c(port=1, address=0x3c)
    device = sh1106(serial, rotate=2)

    logging.basicConfig(filename='/tmp/rpims_serial_display.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger=logging.getLogger(__name__)

    try:
        hostname = socket.gethostname()
        hostip = socket.gethostbyname(hostname)

        while True:
            with canvas(device) as draw:
                #get data from redis db
                values = redis_db.mget('BME280_Temperature', 'BME280_Humidity', 'BME280_Pressure', 'door_sensor_1', 'door_sensor_2', 'CPU_Temperature')
                temperature = round(float(values[0]),1)
                humidity = int(round(float(values[1]),1))
                pressure = int(round(float(values[2]),1))
                door_sensor_1 = values[3]
                door_sensor_2 = values[4]
                cputemp = round(float(values[5]),1)
                #draw on oled
                draw.text((x, top),       'RPiMS IP:' + str(hostip), font=font, fill=255)
                draw.text((x, top+9),     'Temperature..' + str(temperature) + '*C', font=font, fill=255)
                draw.text((x, top+18),    'Humidity.....' + str(humidity) + '%',  font=font, fill=255)
                draw.text((x, top+27),    'Pressure.....' + str(pressure) + 'hPa',  font=font, fill=255)
                draw.text((x, top+36),    'Door 1.......' + str(door_sensor_1),  font=font, fill=255)
                draw.text((x, top+45),    'Door 2.......' + str(door_sensor_2),  font=font, fill=255)
                draw.text((x, top+54),    'CpuTemp......' + str(cputemp) + '*C', font=font, fill=255)
            sleep(1/config['display_refresh_rate'])
    except Exception as err :
        logger.error(err)


def lcd_st7735():
    from luma.core.interface.serial import spi, noop
    from luma.core.render import canvas
    from luma.core import lib
    from luma.lcd.device import st7735
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    from PIL import ImageColor
    #import RPi.GPIO as GPIO
    import time
    import datetime
    import socket
# Load default font.
    font = ImageFont.load_default()
#Display width/height
    width = 128
    height = 128
# First define some constants to allow easy resizing of shapes.
    padding = 0
    top = padding
    bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    logging.basicConfig(filename='/tmp/rpims_serial_display.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger=logging.getLogger(__name__)

    serial = spi(device=0, port=0, bus_speed_hz = 8000000, transfer_size = 4096, gpio_DC = 25, gpio_RST = 27)

    try:
        device = st7735(serial)
        device = st7735(serial, width=128, height=128, h_offset=1, v_offset=2, bgr=True, persist=False)
        hostname = socket.gethostname()
        hostip = socket.gethostbyname(hostname)

        while True:
            #get data from redis db
            values = redis_db.mget('BME280_Temperature', 'BME280_Humidity', 'BME280_Pressure', 'door_sensor_1', 'door_sensor_2', 'CPU_Temperature')
            temperature = round(float(values[0]),1)
            humidity = int(round(float(values[1]),1))
            pressure = int(round(float(values[2]),1))
            door_sensor_1 = values[3]
            door_sensor_2 = values[4]
            cputemp = round(float(values[5]),1)
            now = datetime.datetime.now()
            # Draw
            with canvas(device) as draw:
                draw.text((x+35, top),'R P i M S', font=font, fill="cyan")
                draw.text((x, top+15),' Temperature', font=font, fill="lime")
                #draw.text((x+71, top+15),'', font=font, fill="blue")
                draw.text((x+77, top+15),str(temperature) + ' *C', font=font, fill="lime")

                draw.text((x, top+28),' Humidity',  font=font, fill="lime")
                #draw.text((x+70, top+28),'', font=font, fill="blue")
                draw.text((x+77, top+28),str(humidity) + ' %',  font=font, fill="lime")

                draw.text((x, top+41),' Pressure',  font=font, fill="lime")
                #draw.text((x+70, top+41),'', font=font, fill="blue")
                draw.text((x+77, top+41),str(pressure) + ' hPa',  font=font, fill="lime")

                draw.text((x, top+57),' Door 1',  font=font, fill="yellow")
                #draw.text((x+70, top+57),'', font=font, fill="yellow")
                draw.text((x+77, top+57),str(door_sensor_1),  font=font, fill="yellow")

                draw.text((x, top+70),' Door 2',  font=font, fill="yellow")
                #draw.text((x+70, top+70),'', font=font, fill="yellow")
                draw.text((x+77, top+70),str(door_sensor_2),  font=font, fill="yellow")

                draw.text((x, top+86),' CPUtemp',  font=font, fill="cyan")
                draw.text((x+77, top+86),str(cputemp)+ " *C",  font=font, fill="cyan")

                draw.text((x, top+99),' IP', font=font, fill="cyan")
                draw.text((x+17, top+99),':', font=font, fill="cyan")
                draw.text((x+36, top+99),str(hostip), font=font, fill="cyan")

                draw.text((x+5, top+115),now.strftime("%Y-%m-%d %H:%M:%S"),  font=font, fill="floralwhite")

            sleep(1/config['display_refresh_rate'])
    except Exception as err :
        logger.error(err)


def threading_function(device_type):
    if device_type is 'BME280' :
        t = threading.Thread(target=get_bme280_data, name=device_type)
        t.daemon = True
        t.start()
    if device_type is 'DS18B20' :
        t = threading.Thread(target=get_ds18b20_data, name=device_type)
        t.daemon = True
        t.start()
    if device_type is 'CPUtemp' :
        t = threading.Thread(target=get_cputemp_data, name=device_type)
        t.daemon = True
        t.start()
    if device_type is 'oled_sh1106' :
        t = threading.Thread(target=oled_sh1106, name=device_type)
        t.daemon = True
        t.start()
    if device_type is 'lcd_st7735' :
        t = threading.Thread(target=lcd_st7735, name=device_type)
        t.daemon = True
        t.start()


# --- Main program ---

print('# RPiMS is running #')
print('')

if config['use_picamera'] is yes and config['use_picamera_recording'] is no and  config['use_door_sensor'] is no and config['use_motion_sensor'] is no :
    av_stream('start')

for s in config :
    redis_db.set(s, str(config[s]))
    if config['verbose'] :
        print(s + ' = ' + str(config[s]))
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
        if motion_sensor_list[s].value == 0:
            motion_sensor_when_no_motion(s)
        else:
            motion_sensor_when_motion(s)
    for s in motion_sensor_list:
            motion_sensor_list[s].when_motion = lambda s=s : motion_sensor_when_motion(s)
            motion_sensor_list[s].when_no_motion = lambda s=s : motion_sensor_when_no_motion(s)
    if config['use_led_indicator'] is yes :
        led_list['motion_led'].source = any_values(*motion_sensor_list.values())

if config['use_system_buttons'] is yes :
    system_buttons['shutdown_button'].when_held = shutdown

if config['use_CPU_sensor'] is yes:
    threading_function("CPUtemp")

if config['use_BME280_sensor'] is yes:
    threading_function("BME280")

if config['use_DS18B20_sensor'] is yes:
    threading_function("DS18B20")

if config['use_serial_display'] is yes:
    threading_function(config['serial_display_type'])

pause()
