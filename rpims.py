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
from subprocess import check_call, call
from signal import pause
from time import sleep
import threading
import redis
import smbus2
import logging
import sys
import yaml


# --- Funcions ---
def door_action_closed(door_id):
    redis_db.set(str(door_id), 'close')
    if config['verbose'] is True :
        print("The " + str(door_id) + " has been closed!")
    if config['use_zabbix_sender'] is True :
        zabbix_sender_call('info_when_door_has_been_closed',door_id)
    if config['use_picamera'] is True:
         if detect_no_alarms():
             av_stream('stop')


def door_action_opened(door_id):
    redis_db.set(str(door_id), 'open')
    if config['verbose'] is True :
        print("The " + str(door_id) + " has been opened!")
    if config['use_zabbix_sender'] is True :
        zabbix_sender_call('info_when_door_has_been_opened',door_id)
    if config['use_picamera'] is True :
        if config['use_picamera_recording'] is True:
            av_stream('stop')
            av_recording()
        av_stream('start')


def door_status_open(door_id):
    redis_db.set(str(door_id), 'open')
    if config['verbose'] is True :
        print("The " + str(door_id) + " is opened!")
    if config['use_zabbix_sender'] is True:
        zabbix_sender_call('info_when_door_is_opened',door_id)
    if config['use_picamera'] is True:
        av_stream('start')


def door_status_close(door_id):
    redis_db.set(str(door_id), 'close')
    if config['verbose'] is True :
        print("The " + str(door_id) + " is closed!")
    if config['use_zabbix_sender'] is True :
        zabbix_sender_call('info_when_door_is_closed',door_id)
    if config['use_picamera'] is True:
         if detect_no_alarms():
             av_stream('stop')


def motion_sensor_when_motion(ms_id):
    redis_db.set(str(ms_id), 'motion')
    if config['verbose'] is True :
        print("The " + str(ms_id) + ": motion was detected")
    if config['use_zabbix_sender'] is True :
        zabbix_sender_call('info_when_motion',ms_id)
    if config['use_picamera'] is True:
        av_stream('start')


def motion_sensor_when_no_motion(ms_id):
    redis_db.set(str(ms_id), 'nomotion')
    if config['verbose'] is True :
        print("The " + str(ms_id) + ": no motion")
    if config['use_picamera'] is True:
         if detect_no_alarms():
             av_stream('stop')


def detect_no_alarms():
    if config['use_door_sensor'] is True and config['use_motion_sensor'] is True:
        door_sensor_values = []
        motion_sensor_values = []
        for s in door_sensors_list:
            door_sensor_values.append(door_sensors_list[s].value)
        for s in motion_sensors_list:
            motion_sensor_values.append(int(not motion_sensors_list[s].value))
        if all(door_sensor_values) and all(motion_sensor_values):
            return True
    if config['use_door_sensor'] is True and config['use_motion_sensor'] is False:
        door_sensor_values = []
        for s in door_sensors_list:
            door_sensor_values.append(door_sensors_list[s].value)
        if all(door_sensor_values):
            return True
    if config['use_door_sensor'] is False and config['use_motion_sensor'] is True:
        motion_sensor_values = []
        for s in motion_sensors_list:
            motion_sensor_values.append(int(not motion_sensors_list[s].value))
        if all(motion_sensor_values):
            return True


def av_stream(state):
    call("/home/pi/scripts/RPiMS/videostreamer.sh" + " " +  state, shell=True)


def av_recording():
    call("/home/pi/scripts/RPiMS/videorecorder.sh", shell=True)


def zabbix_sender_call(message,sensor_id):
    zabbix_sender_cmd ='/home/pi/scripts/RPiMS/zabbix_sender.sh ' + message + " " + str(sensor_id)
    call(zabbix_sender_cmd, shell=True)


def hostnamectl_sh():
    call("sudo /home/pi/scripts/RPiMS/hostnamectl.sh", shell=True)


def shutdown():
    check_call(['sudo', 'poweroff'])


def get_cputemp_data():
    try:
        from gpiozero import CPUTemperature
        while True :
            data = CPUTemperature()
            redis_db.set('CPU_Temperature', data.temperature)
            if config['verbose'] is True :
                print('CPU temperature: {0:0.1f}'.format(data.temperature),chr(176)+'C', sep='')
                print("")
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
            if config['verbose'] is True :
                print('')
                print('BME280 Humidity: {0:0.0f}%'.format(data.humidity))
                print('BME280 Temperature: {0:0.1f}\xb0C'.format(data.temperature))
                print('BME280 Pressure: {0:0.0f}hPa'.format(data.pressure))
                print("")
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
                if config['verbose'] is True :
                    print("Sensor %s temperature %.2f"%(sensor.id,sensor.get_temperature()),"\xb0C")
                    print("")
            sleep(config['DS18B20_read_interval'])
    except Exception as err :
        logger.error(err)
        print('Problem with ' + str(err))


def get_dht_data():
    import adafruit_dht
    pin = config['DHT_pin']
    debug = "yes"
    delay = 0

    if config['DHT_type'] is "DHT22":
        dhtDevice = adafruit_dht.DHT22(pin)
    if config['DHT_type'] is "DHT11":
        dhtDevice = adafruit_dht.DHT11(pin)

    while True:
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            redis_db.mset({'DHT_Humidity' : humidity,'DHT_Temperature' : temperature,})
            if config['verbose'] is True :
                print(config['DHT_type'] + " Temperature: {:.1f} °C ".format(temperature))
                print(config['DHT_type'] + " Humidity: {}% ".format(humidity))
                print("")
            delay -= 1
            if delay < 0:
                delay = 0
        except RuntimeError as error:
            if debug is 'yes':
                print("DHT - " + str(error.args[0]))
            delay += 1
        finally:
            if debug is 'yes':
                print("DHT delay: " + str(delay))
            redis_db.set('DHT_delay', delay)
            sleep(config['DHT_read_interval']+delay)


def oled_sh1106():
    from luma.core.interface.serial import i2c, noop
    from luma.core.render import canvas
    from luma.core import lib
    from luma.oled.device import sh1106
    #from PIL import Image
    #from PIL import ImageDraw
    from PIL import ImageFont
    import time
    #import socket

    # Load default font.
    font = ImageFont.load_default()
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = 128
    height = 64
    #image = Image.new('1', (width, height))
    # First define some constants to allow easy resizing of shapes.
    padding = 0
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    logging.basicConfig(filename='/tmp/rpims_serial_display.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger=logging.getLogger(__name__)

    serial = i2c(port=1, address=0x3c)

    try:
        device = sh1106(serial, rotate=0)

        while True:
            with canvas(device) as draw:
                #get data from redis db
                values = redis_db.mget('BME280_Temperature', 'BME280_Humidity', 'BME280_Pressure', 'door_sensor_1', 'door_sensor_2', 'CPU_Temperature', 'hostip')
                temperature = round(float(values[0]),1)
                humidity = int(round(float(values[1]),1))
                pressure = int(round(float(values[2]),1))
                door_sensor_1 = values[3]
                door_sensor_2 = values[4]
                cputemp = round(float(values[5]),1)
                hostip = values[6]
                #draw on oled
                draw.text((x, top),       'IP:' + str(hostip), font=font, fill=255)
                draw.text((x, top+9),     'Temperature..' + str(temperature) + '*C', font=font, fill=255)
                draw.text((x, top+18),    'Humidity.....' + str(humidity) + '%',  font=font, fill=255)
                draw.text((x, top+27),    'Pressure.....' + str(pressure) + 'hPa',  font=font, fill=255)
                draw.text((x, top+36),    'Door 1.......' + str(door_sensor_1),  font=font, fill=255)
                draw.text((x, top+45),    'Door 2.......' + str(door_sensor_2),  font=font, fill=255)
                draw.text((x, top+54),    'CpuTemp......' + str(cputemp) + '*C', font=font, fill=255)
            sleep(1/config['serial_display_refresh_rate'])
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
    #import socket
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

        while True:
            #get data from redis db
            values = redis_db.mget('BME280_Temperature', 'BME280_Humidity', 'BME280_Pressure', 'door_sensor_1', 'door_sensor_2', 'CPU_Temperature', 'hostip')
            temperature = round(float(values[0]),1)
            humidity = int(round(float(values[1]),1))
            pressure = int(round(float(values[2]),1))
            door_sensor_1 = values[3]
            door_sensor_2 = values[4]
            cputemp = round(float(values[5]),1)
            hostip = values[6]
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

            sleep(1/config['serial_display_refresh_rate'])
    except Exception as err :
        logger.error(err)


def threading_function(function_name):
    t = threading.Thread(target=function_name, name=function_name)
    t.daemon = True
    t.start()


# --- Main program ---

print('# RPiMS is running #')
print('')

try:
    with open(r'/home/pi/scripts/RPiMS/rpims.yaml') as file:
        config_yaml = yaml.full_load(file)

except Exception as err :
    logger.error(err)
    print('Problem with ' + str(err))
    sys.exit(1)


config = {}
door_sensors_list = {}
motion_sensors_list = {}
system_buttons_list = {}
led_indicators_list = {}

for item in config_yaml.get("setup"):
    config[item] = config_yaml['setup'][item]

if config['use_door_sensor'] is True:
    for item in config_yaml.get("door_sensors"):
        door_sensors_list[item] = Button(config_yaml['door_sensors'][item]['gpio_pin'], hold_time=config_yaml['door_sensors'][item]['hold_time'])

if config['use_motion_sensor'] is True:
    for item in config_yaml.get("motion_sensors"):
        motion_sensors_list[item] = MotionSensor(config_yaml['motion_sensors'][item]['gpio_pin'])

if config['use_system_buttons'] is True:
    for item in config_yaml.get("system_buttons"):
        system_buttons_list[item] = Button(config_yaml['system_buttons'][item]['gpio_pin'], hold_time=config_yaml['system_buttons'][item]['hold_time'])

if config['use_led_indicator'] is True:
    for item in config_yaml.get("led_indicators"):
        led_indicators_list[item] = LED(config_yaml['led_indicators'][item]['gpio_pin'])


redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)

logging.basicConfig(filename='/tmp/rpims.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)


for s in config :
    redis_db.set(s, str(config[s]))
    if config['verbose'] is True :
        print(s + ' = ' + str(config[s]))
print('')

hostnamectl_sh()

if config['use_door_sensor'] is True :
    for s in door_sensors_list:
        if door_sensors_list[s].value == 0:
            door_status_open(s)
        else:
            door_status_close(s)
    for s in door_sensors_list:
            door_sensors_list[s].when_held = lambda s=s : door_action_closed(s)
            door_sensors_list[s].when_released = lambda s=s : door_action_opened(s)
    if config['use_led_indicator'] is True :
        led_indicators_list['door_led'].source = all_values(*door_sensors_list.values())

if config['use_motion_sensor'] is True :
    for s in motion_sensors_list:
        if motion_sensors_list[s].value == 0:
            motion_sensor_when_no_motion(s)
        else:
            motion_sensor_when_motion(s)
    for s in motion_sensors_list:
            motion_sensors_list[s].when_motion = lambda s=s : motion_sensor_when_motion(s)
            motion_sensors_list[s].when_no_motion = lambda s=s : motion_sensor_when_no_motion(s)
    if config['use_led_indicator'] is True :
        led_indicators_list['motion_led'].source = any_values(*motion_sensors_list.values())

if config['use_system_buttons'] is True :
    system_buttons_list['shutdown_button'].when_held = shutdown

if config['use_CPU_sensor'] is True:
    threading_function(get_cputemp_data)

if config['use_BME280_sensor'] is True:
    threading_function(get_bme280_data)

if config['use_DS18B20_sensor'] is True:
    threading_function(get_ds18b20_data)

if config['use_DHT_sensor'] is True:
    threading_function(get_dht_data)

if config['use_serial_display'] is True:
    if config['serial_display_type'] == 'oled_sh1106':
        threading_function(oled_sh1106)
    if config['serial_display_type'] == 'lcd_st7735':
        threading_function(lcd_st7735)

if config['use_picamera'] is True and config['use_picamera_recording'] is False and config['use_door_sensor'] is False and config['use_motion_sensor'] is False :
    av_stream('start')

pause()
