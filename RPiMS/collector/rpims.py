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

import os
import sys
import adafruit_dht
import adafruit_ads1x15.ads1115 as ADS
import automationhat
import bme280
import board
import busio
import datetime
import json
import logging
import math
import multiprocessing
import fcntl
import redis
import smbus2
import subprocess
import sys
import serial
import setproctitle
import statistics
import threading
import usb.core
import yaml
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import LED, Button, MotionSensor, CPUTemperature
from gpiozero.tools import all_values, any_values
from grove.i2c import Bus
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106
from luma.lcd.device import st7735
from PIL import ImageFont
from serial.serialutil import SerialException
from signal import pause
from time import time, sleep
from w1thermsensor import W1ThermSensor


logging.basicConfig(
    level=logging.INFO,
    format="RPiMS-collector: %(levelname)s: %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger("RPiMS-collector")


class AppContext:
    def __init__(self, gpio, config, zabbix_agent, sensors, redis_db):
        self.gpio = gpio
        self.config = config
        self.zabbix_agent = zabbix_agent
        self.sensors = sensors
        self.redis_db = redis_db

        # sensors subset:
        self.bme280_config = sensors['BME280']
        self.dht_config = sensors['DHT']
        self.cputemp_config = sensors['CPU']['temp']
        self.ds18b20_config = sensors['ONE_WIRE']['DS18B20']
        self.rainfall_config = sensors['WEATHER']['RAINFALL']
        self.windspeed_config = sensors['WEATHER']['WIND']['SPEED']
        self.winddirection_config = sensors['WEATHER']['WIND']['DIRECTION']

        # gpio supsets
        self.door_sensors = {}
        self.motion_sensors = {}
        self.system_buttons = {}
        self.led_indicators = {}


class SensorContext:
    def __init__(self, app_context, sensor_name, sensor_config):
        self.app = app_context          # global AppContext
        self.name = sensor_name         # for example "id3"
        self.config = sensor_config     # config specific sensor


# --- Functions ---
def acquire_lock(lock_path="/run/lock/rpims.lock"):
    try:
        fp = open(lock_path, "w")
    except PermissionError:
        logger.error(f"Cannot open lock file {lock_path}. Check permissions.")
        sys.exit(1)

    try:
        fcntl.flock(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        logger.error("Another instance of RPiMS is already running. Exiting.")
        sys.exit(1)

    return fp  # keep file descriptor open!


def init_door_sensors(ctx: AppContext):
    sensors = {}
    if ctx.config.get('use_door_sensor'):
        for item, cfg in ctx.gpio.items():
            if cfg['type'] == 'DoorSensor':
                sensors[item] = Button(cfg['pin'], hold_time=int(cfg['hold_time']))
    return sensors


def init_motion_sensors(ctx: AppContext):
    sensors = {}
    if ctx.config.get('use_motion_sensor'):
        for item, cfg in ctx.gpio.items():
            if cfg['type'] == 'MotionSensor':
                sensors[item] = MotionSensor(cfg['pin'])
    return sensors


def init_system_buttons(ctx: AppContext):
    buttons = {}
    if ctx.config.get('use_system_buttons'):
        for item, cfg in ctx.gpio.items():
            if cfg['type'] == 'ShutdownButton':
                buttons['shutdown_button'] = Button(cfg['pin'], hold_time=int(cfg['hold_time']))
    return buttons


def init_led_indicators(ctx: AppContext):
    leds = {}
    for item, cfg in ctx.gpio.items():
        if cfg['type'] == 'door_led':
            leds['door_led'] = LED(cfg['pin'])
        elif cfg['type'] == 'motion_led':
            leds['motion_led'] = LED(cfg['pin'])
        elif cfg['type'] == 'led':
            leds['led'] = LED(cfg['pin'])
    return leds


def door_action_closed(ctx, door_id):
    ctx.redis_db.hset('GPIO', str(door_id), 'close')
    ctx.redis_db.hset('DOOR_SENSORS', str(door_id), 'close')

    if ctx.config.get('verbose'):
        logger.info(f'The {door_id} has been closed!')

    if ctx.config.get('use_zabbix_sender'):
        zabbix_sender_call('info_when_door_has_been_closed', door_id)

def door_action_opened(ctx, door_id):
    ctx.redis_db.hset('GPIO', str(door_id), 'open')
    ctx.redis_db.hset('DOOR_SENSORS', str(door_id), 'open')

    if ctx.config.get('verbose'):
        logger.info(f'The {door_id} has been opened!')

    if ctx.config.get('use_zabbix_sender'):
        zabbix_sender_call('info_when_door_has_been_opened', door_id)

    if ctx.config.get('use_picamera'):
        if ctx.config.get('use_picamera_recording'):
            av_recording()

def door_status_open(ctx, door_id):
    ctx.redis_db.hset('GPIO', str(door_id), 'open')
    ctx.redis_db.hset('DOOR_SENSORS', str(door_id), 'open')

    if ctx.config.get('verbose'):
        logger.info(f'The {door_id} is opened!')

    if ctx.config.get('use_zabbix_sender'):
        zabbix_sender_call('info_when_door_is_opened', door_id)


def door_status_close(ctx, door_id):
    ctx.redis_db.hset('GPIO', str(door_id), 'close')
    ctx.redis_db.hset('DOOR_SENSORS', str(door_id), 'close')

    if ctx.config.get('verbose'):
        logger.info(f'The {door_id} is closed!')

    if ctx.config.get('use_zabbix_sender'):
        zabbix_sender_call('info_when_door_is_closed', door_id)

def motion_sensor_when_motion(ctx, ms_id):
    ctx.redis_db.hset('GPIO', str(ms_id), 'motion')
    ctx.redis_db.hset('MOTION_SENSORS', str(ms_id), 'motion')

    if ctx.config.get('verbose'):
        logger.info(f'The {ms_id} : motion was detected!')

    if ctx.config.get('use_zabbix_sender'):
        zabbix_sender_call('info_when_motion', ms_id)

    if ctx.config.get('use_picamera'):
        if ctx.config.get('use_picamera_recording'):
            av_recording()


def motion_sensor_when_no_motion(ctx, ms_id):
    ctx.redis_db.hset('GPIO', str(ms_id), 'nomotion')
    ctx.redis_db.hset('MOTION_SENSORS', str(ms_id), 'nomotion')

    if ctx.config.get('verbose'):
        logger.info(f'The {ms_id} : no motion')


def detect_no_alarms(ctx):
    use_door = ctx.config.get('use_door_sensor')
    use_motion = ctx.config.get('use_motion_sensor')

    # both type door and motion sensors are active
    if use_door and use_motion:
        door_values = [sensor.value for sensor in ctx.door_sensors.values()]
        motion_values = [int(not sensor.value) for sensor in ctx.motion_sensors.values()]
        return all(door_values) and all(motion_values)

    # only door sensors
    if use_door and not use_motion:
        door_values = [sensor.value for sensor in ctx.door_sensors.values()]
        return all(door_values)

    # only motion sensors
    if not use_door and use_motion:
        motion_values = [int(not sensor.value) for sensor in ctx.motion_sensors.values()]
        return all(motion_values)

    # no sensors = no alarms
    return True


def av_stream(state):
    # _cmd = '../scripts/videostreamer.sh' + " " + state
    _cmd = f'sudo systemctl {state} mediamtx.service'
    subprocess.call(_cmd, shell=True)


def av_recording():
    _cmd = '../scripts/videorecorder.sh'
    subprocess.Popen([_cmd],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=True)


def zabbix_sender_call(message, sensor_id):
    _cmd = '../scripts/zabbix_sender.sh ' + message + " " + str(sensor_id)
    subprocess.Popen([_cmd],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=True)


def hostnamectl_sh(**kwargs):
    hctldict = {
        "location": "set-location",
        "chassis": "set-chassis",
        "deployment": "set-deployment",
    }

    # set hostname
    hostname = kwargs.get('hostname')
    if hostname:
        subprocess.call([
            'sudo', 'raspi-config', 'nonint', 'do_hostname', hostname
        ])

    # use hostnamectl
    for key, action in hctldict.items():
        value = kwargs.get(key)
        if value:
            subprocess.call([
                'sudo', '/usr/bin/hostnamectl', action, value
            ])


def get_hostip():
    _cmd = 'sudo ../scripts/gethostinfo.sh'
    subprocess.call(_cmd, shell=True)


def shutdown():
    subprocess.check_call(['sudo', 'poweroff'])


def get_cputemp_data(ctx):
    verbose = ctx.config.get('verbose')
    read_interval = ctx.cputemp_config.get('read_interval')

    try:
        while True:
            data = CPUTemperature()
            ctx.redis_db.set('CPU_Temperature', data.temperature)
            ctx.redis_db.expire('CPU_Temperature', read_interval * 2)

            if verbose:
                logger.info(f"CPU temperature: {data.temperature:0.1f}{chr(176)}C")

            sleep(read_interval)

    except Exception as err:
        logger.info(f'Problem with CPU sensor: {err}')


def get_bme280_data(sensor_ctx):
    app = sensor_ctx.app
    redis_db = app.redis_db
    verbose = app.config.get('verbose')

    sid = sensor_ctx.name
    cfg = sensor_ctx.config

    read_interval = cfg.get('read_interval')
    interface_type = cfg.get('interface')
    
    # --- I2C MODE ---
    if interface_type == 'i2c':
        try:
            port = 1
            address = cfg.get('i2c_address')
            bus = smbus2.SMBus(port)
            calibration_params = bme280.load_calibration_params(bus, address)

            while True:
                try:
                    data = bme280.sample(bus, address, calibration_params)

                    temperature = round(data.temperature, 3)
                    humidity = round(data.humidity, 3)
                    pressure = round(data.pressure, 3)

                    key = f'{sid}_BME280'
                    redis_db.hset(key, 'temperature', temperature)
                    redis_db.hset(key, 'humidity', humidity)
                    redis_db.hset(key, 'pressure', pressure)
                    redis_db.expire(key, read_interval * 2)

                    if verbose:
                        logger.info(
                            f'{sid}_BME280: Temperature: {temperature} °C, '
                            f'Humidity: {humidity} %, Pressure: {pressure} hPa'
                        )

                    sleep(read_interval)

                except (KeyboardInterrupt, SystemExit):
                    break

                except Exception as err:
                    logger.info(f'Problem with sensor BME280: {err}')
                    sleep(1)

        except Exception as err:
            logger.info(f'Problem initializing BME280 I2C: {err}')
    # --- SERIAL MODE ---
    if interface_type == 'serial':
        usbport = cfg.get('serial_port')

        # detect RPi model
        devicetree = subprocess.check_output(
            ["cat /sys/firmware/devicetree/base/model"],
            shell=True
        ).decode('UTF-8').split(' ')
        rpimodel = devicetree[2]

        # serial port maps
        rpi3_serial_ports_by_path = {
            '3': {
                'USB1': '/dev/serial/by-path/platform-3f980000.usb-usb-0:1.1.2:1.0',
                'USB2': '/dev/serial/by-path/platform-3f980000.usb-usb-0:1.1.3:1.0',
                'USB3': '/dev/serial/by-path/platform-3f980000.usb-usb-0:1.2:1.0',
                'USB4': '/dev/serial/by-path/platform-3f980000.usb-usb-0:1.3:1.0',
            }
        }

        rpi4_serial_ports_by_path = {
            '4': {
                'USB1': '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0',
                'USB2': '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0',
                'USB3': '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0',
                'USB4': '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.4:1.0',
            }
        }

        rpi400_serial_ports_by_path = {
            '400': {
                'USB1': '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0',
                'USB2': '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0',
                'USB3': '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0',
            }
        }

        rpi_serial_ports_by_path = {
            **rpi3_serial_ports_by_path,
            **rpi4_serial_ports_by_path,
            **rpi400_serial_ports_by_path
        }

        try:
            serial_port = rpi_serial_ports_by_path.get(rpimodel).get(usbport)
        except:
            logger.error('Unknown serial device')
            sys.exit(1)

        lecounter = 0
        necounter = 0

        # --- USB reset helper ---
        def reset_usbdevice():
            devices = usb.core.find(find_all=True)
            for item in devices:
                if hex(item.idVendor) == '0x2e8a':
                    item.reset()

        # --- find serial device ---
        def find_serial_device(port, baudrate):
            while True:
                try:
                    ser = serial.Serial(
                        port, baudrate,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        xonxoff=False,
                        rtscts=False,
                        dsrdtr=True,
                        timeout=1
                    )
                    logger.info('Serial device found')
                    return ser
                except SerialException:
                    logger.info(f"BME280PicoUSB not connected to port {usbport}")
                    sleep(2)
                except Exception as err:
                    logger.info(f"Resetting USB port for BME280PicoUSB on {usbport}")
                    logger.error(err)
                    reset_usbdevice()
                    sleep(10)

        # --- serial data generator ---
        def serial_data(port, baudrate):
            while True:
                try:
                    ser = serial.Serial(
                        port, baudrate,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        xonxoff=False,
                        rtscts=False,
                        dsrdtr=True,
                        timeout=3
                    )
                    logger.info('Serial device found')
                    break
                except Exception:
                    logger.info(f"Could not open BME280PicoUSB on port {usbport}")
                    sleep(1)

            ser.flushInput()
            ser.write(b'\x03')
            ser.write(b'\x04')
            sleep(1)
            ser.close()
            sleep(1)

            while True:
                try:
                    ser = serial.Serial(
                        port, baudrate,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        xonxoff=False,
                        rtscts=False,
                        dsrdtr=True,
                        timeout=3
                    )
                    sleep(3)

                    while ser.inWaiting() > 0:
                        ser.flushInput()
                        response = ser.readline()
                        yield response
                    else:
                        sleep(0.5)

                except Exception:
                    logger.info(f"Lost connection with BME280PicoUSB on port {usbport}")
                    find_serial_device(port, baudrate)
                    sleep(2)

        # --- main serial loop ---
        for line in serial_data(serial_port, 115200):
            msg = line.decode('utf-8').split()

            if len(msg) < 4:
                lecounter += 1
                ctx.redis_db.set('LECOUNTER', lecounter)
                continue

            if msg[0] != "BME280":
                continue

            t, h, p = msg[1], msg[2], msg[3]

            if t.isnumeric() and h.isnumeric() and p.isnumeric():
                temperature = int(t) / 1000
                humidity = int(h) / 1000
                pressure = int(p) / 1000

                key = f'{sid}_BME280'
                redis_db.hset(key, 'temperature', temperature)
                redis_db.hset(key, 'humidity', humidity)
                redis_db.hset(key, 'pressure', pressure)

                expire_time = 10 if read_interval < 10 else read_interval * 2
                redis_db.expire(key, expire_time)

                if verbose:
                    logger.info(
                        f'{sid}_BME280: Temperature: {temperature}°C, '
                        f'Humidity: {humidity}%, Pressure: {pressure}hPa'
                    )
            else:
                necounter += 1
                redis_db.set('NECOUNTER', necounter)

            sleep(read_interval)


def get_ds18b20_data(ctx):
    verbose = ctx.config.get('verbose')
    read_interval = ctx.ds18b20_config.get('read_interval')

    try:
        while True:
            sensors = W1ThermSensor.get_available_sensors()

            for sensor in sensors:
                temperature = sensor.get_temperature()
                ctx.redis_db.hset('DS18B20', sensor.id, temperature)

                if verbose:
                    logger.info(f"Sensor {sensor.id} temperature {temperature:.2f}{chr(176)}C")

            # data expiration time setting
            expire_time = 10 if read_interval < 5 else read_interval * 2
            ctx.redis_db.expire('DS18B20', expire_time)

            sleep(read_interval)

    except Exception as err:
        logger.info(f'Problem with sensor DS18B20: {err}')


def get_dht_data(ctx):
    verbose = ctx.config.get('verbose')
    read_interval = ctx.dht_config.get('read_interval')
    dht_type = ctx.dht_config.get('type')
    pin = ctx.dht_config.get('pin')

    debug = "no"
    delay = 0

    # selection of DHT model
    if dht_type == "DHT11":
        dht_device = adafruit_dht.DHT11(pin)
    else:
        dht_device = adafruit_dht.DHT22(pin)

    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            ctx.redis_db.hset('DHT', 'temperature', temperature)
            ctx.redis_db.hset('DHT', 'humidity', humidity)
            ctx.redis_db.expire('DHT', read_interval * 3)

            if verbose:
                logger.info(f"{dht_type} Temperature: {temperature:.1f}°C")
                logger.info(f"{dht_type} Humidity: {humidity}%")

            delay = max(delay - 1, 0)

        except OverflowError as err:
            if debug == 'yes':
                logger.info(f'Problem with DHT sensor: {err}')
            delay += 1

        except RuntimeError as err:
            if debug == 'yes':
                logger.info(f'Problem with DHT sensor - {err}')
            delay += 1

        except Exception as err:
            dht_device.exit()
            raise err

        finally:
            if debug == 'yes':
                logger.info(f'DHT delay: {delay}')

            ctx.redis_db.set('DHT_delay', delay)
            sleep(read_interval + delay)


def rainfall(ctx):
    # configuration
    verbose = ctx.config.get('verbose')
    sensor_pin = ctx.rainfall_config.get('sensor_pin')
    acquisition_time = ctx.rainfall_config.get('acquisition_time')
    aggregation_time = ctx.rainfall_config.get('agregation_time')

    BUCKET_SIZE = 0.2794  # mm per tilt
    bucket_counter = 0
    rainfalls = []

    # helper functions
    def bucket_tipped():
        nonlocal bucket_counter
        bucket_counter += 1

    def reset_bucket_counter():
        nonlocal bucket_counter
        bucket_counter = 0

    def calculate_rainfall():
        return round(bucket_counter * BUCKET_SIZE, 0)

    # sensor initialisation
    rain_sensor = Button(sensor_pin)
    rain_sensor.when_pressed = bucket_tipped

    # setting initial values in Redis
    ctx.redis_db.hset('WEATHER', 'daily_rainfall', 0)
    ctx.redis_db.hset('WEATHER', 'rainfall', 0)

    # main loop
    while True:
        start_time = time()

        while time() - start_time <= acquisition_time:
            reset_bucket_counter()
            sleep(acquisition_time)

            rainfall_value = calculate_rainfall()

            # limit on the list length
            if len(rainfalls) == (aggregation_time / acquisition_time):
                rainfalls.clear()

            rainfalls.append(rainfall_value)

        daily_rainfall = round(math.fsum(rainfalls), 1)

        if verbose:
            logger.info(f'Rainfall: {rainfall_value}mm, Daily rainfall: {daily_rainfall}mm')

        ctx.redis_db.hset('WEATHER', 'daily_rainfall', daily_rainfall)
        ctx.redis_db.hset('WEATHER', 'rainfall', rainfall_value)


def wind_speed(ctx):
    verbose = ctx.config.get('verbose')

    sensor_pin = ctx.windspeed_config.get('sensor_pin')
    acquisition_time = ctx.windspeed_config.get('acquisition_time')
    aggregation_time = ctx.windspeed_config.get('agregation_time')

    ANEMOMETER_FACTOR = 1.18

    anemometer_pulse = 0
    wind_speeds = []
    average_wind_speeds = []
    daily_wind_gusts = []

    # helper functions
    def anemometer_pulse_counter():
        nonlocal anemometer_pulse
        anemometer_pulse += 1

    def reset_anemometer_pulse_counter():
        nonlocal anemometer_pulse
        anemometer_pulse = 0

    def calculate_speed():
        rotations = anemometer_pulse / 2
        return round(ANEMOMETER_FACTOR * rotations * 2.4 / acquisition_time, 1)

    # sensors initialisation
    wind_speed_sensor = Button(sensor_pin)
    wind_speed_sensor.when_pressed = anemometer_pulse_counter

    # initial values
    init_values = {
        'wind_speed': 0,
        'wind_gust': 0,
        'daily_wind_gust': 0,
        'average_wind_speed': 0,
        'daily_average_wind_speed': 0
    }
    ctx.redis_db.hset('WEATHER', mapping=init_values)

    # main loop
    while True:
        start_time = time()

        while time() - start_time <= acquisition_time:
            reset_anemometer_pulse_counter()
            sleep(acquisition_time)

            speed = calculate_speed()
            ctx.redis_db.hset('WEATHER', 'wind_speed', speed)

            # short-term aggregation
            if len(wind_speeds) == (aggregation_time / acquisition_time):
                wind_speeds.pop(0)

            wind_speeds.append(speed)

        # widn gust
        wind_gust = max(wind_speeds)
        ctx.redis_db.hset('WEATHER', 'wind_gust', wind_gust)

        # daily wind gust
        if len(daily_wind_gusts) == (86400 / acquisition_time):
            daily_wind_gusts.pop(0)

        daily_wind_gusts.append(wind_gust)
        daily_gust = max(daily_wind_gusts)
        ctx.redis_db.hset('WEATHER', 'daily_wind_gust', daily_gust)

        # average speed
        avg_speed = round(statistics.mean(wind_speeds), 1)
        ctx.redis_db.hset('WEATHER', 'average_wind_speed', avg_speed)

        # average daily wind speed
        if len(average_wind_speeds) == (86400 / aggregation_time):
            average_wind_speeds.pop(0)

        average_wind_speeds.append(avg_speed)
        daily_avg_speed = round(statistics.mean(average_wind_speeds), 1)
        ctx.redis_db.hset('WEATHER', 'daily_average_wind_speed', daily_avg_speed)

        if verbose:
            logger.info(
                f"Wind speed: {speed} km/h, "
                f"Wind gust: {wind_gust} km/h, "
                f"Daily wind gust: {daily_gust} km/h, "
                f"Average wind speed: {avg_speed} km/h, "
                f"Daily average wind speed: {daily_avg_speed} km/h"
            )


def adc_stm32f030():
    ADC_DEFAULT_IIC_ADDR = 0X04
    ADC_CHAN_NUM = 8

    # REG_RAW_DATA_START = 0X10
    REG_VOL_START = 0X20
    # REG_RTO_START = 0X30

    # REG_SET_ADDR = 0XC0

    class Pi_hat_adc():
        def __init__(self, bus_num=1, addr=ADC_DEFAULT_IIC_ADDR):
            self.bus = Bus(bus_num)
            self.addr = addr

        def get_all_vol_milli_data(self):
            array = []
            for i in range(ADC_CHAN_NUM):
                data = self.bus.read_i2c_block_data(self.addr, REG_VOL_START+i, 2)
                val = data[1] << 8 | data[0]
                array.append(val)
            return array

        def get_nchan_vol_milli_data(self, n):
            data = self.bus.read_i2c_block_data(self.addr, REG_VOL_START+n, 2)
            val = data[1] << 8 | data[0]
            return val

    adc = Pi_hat_adc()
    adc_inputs_values = adc.get_all_vol_milli_data()
    return adc_inputs_values



def adc_automationphat():
    try:
        sleep(0.1)  # Delay for automationhat
        adc_inputs_values = [automationhat.analog.one.read(), automationhat.analog.two.read(),
                             automationhat.analog.three.read()]
        return adc_inputs_values
    except Exception as err:
        logger.error(err)
        logger.error('automationphat is not detected')
        sys.exit(1)


def adc_ads1115():
    try:
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)
        chan1 = AnalogIn(ads, ADS.P0)
        chan2 = AnalogIn(ads, ADS.P1)
        chan3 = AnalogIn(ads, ADS.P2)
        chan4 = AnalogIn(ads, ADS.P3)
        adc_inputs_values = [chan1.voltage, chan2.voltage, chan3.voltage, chan4.voltage]
        return adc_inputs_values
    except Exception as err:
        logger.error(err)
        logger.error('adc_ads1115 is not detected')
        sys.exit(1)



def wind_direction(ctx):
    # configuration
    verbose = ctx.config.get('verbose')
    acquisition_time = ctx.winddirection_config.get('acquisition_time')
    adc_type = ctx.winddirection_config.get('adc_type')
    adc_input = ctx.winddirection_config.get('adc_input')
    reference_input = ctx.winddirection_config.get('reference_voltage_adc_input')

    # initial values
    ctx.redis_db.hset('WEATHER', 'wind_direction', 0)
    ctx.redis_db.hset('WEATHER', 'average_wind_direction', 0)

    # resistance and angle maps
    direction_mapr = {
        "N": 5080, "NNE": 5188, "NE": 6417, "ENE": 6253,
        "E": 17419, "ESE": 9380, "SE": 11613, "SSE": 6968,
        "S": 8129, "SSW": 5419, "SW": 5542, "W": 4781,
        "NW": 4977, "NNW": 4877,
    }

    direction_mapa = {
        "N": 0, "NNE": 22.5, "NE": 45, "ENE": 67.5,
        "E": 90, "ESE": 112.5, "SE": 135, "SSE": 157.5,
        "S": 180, "SSW": 202.5, "SW": 225, "W": 270,
        "NW": 315, "NNW": 337.5,
    }

    # constant values
    r1 = 4690
    uin = 5.2
    uout = 0

    # auxiliary function for calculating the average direction
    def get_average(angles):
        sin_sum = sum(math.sin(math.radians(a)) for a in angles)
        cos_sum = sum(math.cos(math.radians(a)) for a in angles)

        s = sin_sum / len(angles)
        c = cos_sum / len(angles)

        arc = math.degrees(math.atan(s / c))

        if s > 0 and c > 0:
            avg = arc
        elif c < 0:
            avg = arc + 180
        elif s < 0 < c:
            avg = arc + 360
        else:
            avg = 0

        return 0 if avg == 360 else avg

    # main loop
    while True:
        start_time = time()
        angles = []

        while time() - start_time <= acquisition_time:

            # ADC selection
            if adc_type == 'AutomationPhat':
                adc_values = adc_automationphat()
            elif adc_type == 'STM32F030':
                adc_values = adc_stm32f030()
            elif adc_type == 'ADS1115':
                adc_values = adc_ads1115()
            else:
                logger.error(f"Unknown ADC type: {adc_type}")
                sleep(1)
                continue

            # selection of the measurement channel
            uout = round(adc_values[adc_input - 1], 1)
            uin = round(adc_values[reference_input - 1], 1)

            # calculation of resistance R2
            if uin != uout and uin != 0:
                r2 = int(r1 / (1 - uout / uin))
            else:
                continue

            # matching resistance to direction
            for key, ref_r in direction_mapr.items():
                if ref_r * 0.995 <= r2 <= ref_r * 1.005:
                    angles.append(direction_mapa[key])

        # calculation of the average direction
        if angles:
            avg_dir = int(round(get_average(angles), 0))

            if verbose:
                logger.info(f'Average Wind Direction: {avg_dir}')

            ctx.redis_db.hset('WEATHER', 'wind_direction', key)
            ctx.redis_db.hset('WEATHER', 'average_wind_direction', avg_dir)


def read_bme280(ctx, sid, default=None):
    raw = ctx.redis_db.hgetall(f"{sid}_BME280")
    #logger.info(f'{raw}')

    if not raw:
        return {
            "temperature": default,
            "humidity": default,
            "pressure": default
        }

    def to_float(v):
        try:
            return float(v)
        except:
            return default

    temp = to_float(raw.get("temperature"))
    hum  = to_float(raw.get("humidity"))
    pres = to_float(raw.get("pressure"))

    return {
        "temperature": round(temp, 1) if temp is not None else default,
        "humidity":    round(hum)     if hum  is not None else default,
        "pressure":    round(pres)    if pres is not None else default,
    }


def serial_displays(ctx):
    display_type = ctx.config.get('serial_display_type')
    rotate = ctx.config.get('serial_display_rotate')
    refresh_rate = ctx.config.get('serial_display_refresh_rate')
    serial_type = ctx.config.get('serial_type')

    font = ImageFont.load_default()
    padding = 0
    top = padding
    x = 0

    # interface selection
    if serial_type == 'i2c':
        serial = i2c(port=1, address=0x3c)
    else:
        serial = spi(
            device=0,
            port=0,
            bus_speed_hz=8000000,
            transfer_size=4096,
            gpio_DC=24 if display_type == 'oled_sh1106' else 25,
            gpio_RST=25 if display_type == 'oled_sh1106' else 27
        )

    try:
        # device selection
        if display_type == 'oled_sh1106':
            device = sh1106(serial, rotate=rotate)

        elif display_type == 'lcd_st7735':
            device = st7735(
                serial,
                width=128,
                height=128,
                h_offset=1,
                v_offset=2,
                bgr=True,
                persist=False,
                rotate=rotate
            )

        else:
            logger.error(f"Unknown serial display type: {display_type}")
            return

        data_refresh_rate = 1
        last_fetch = 0
        # main display loop 
        while True:
            now = time()
            if now - last_fetch >= 1/data_refresh_rate: 
                sid = 'id3'

                # reading data from Redis
                bme280 = read_bme280(ctx,sid)
                t,h,p = bme280["temperature"],bme280["humidity"],bme280["pressure"]
                #logger.info(f'{bme280}')
                # door and motion
                values = ctx.redis_db.hgetall('GPIO')
                doors_opened = any(v == 'open' for v in values.values())
                motion_detected = any(v == 'motion' for v in values.values())

                door_sensors = 'opened' if doors_opened else 'closed'
                motion_sensors = 'yes' if motion_detected else 'no'

                # CPU temp
                cputemp = ctx.redis_db.get('CPU_Temperature')
                cputemp = '----' if cputemp is None else round(float(cputemp), 1)

                # IP
                hostip = ctx.redis_db.get('hostip')
                hostip = hostip if hostip else '---.---.---.---'
                last_fetch = now

            # drawing
            label_x = 0
            value_x = 77

            with canvas(device) as draw:
                if display_type == 'oled_sh1106':
                    draw.text((label_x, top),     "IP:", font=font, fill=255)
                    draw.text((15, top),     hostip, font=font, fill=255)

                    draw.text((label_x, top+9),   "Temperature:", font=font, fill=255)
                    draw.text((value_x, top+9),   f"{t}°C", font=font, fill=255)

                    draw.text((label_x, top+18),  "Humidity:", font=font, fill=255)
                    draw.text((value_x, top+18),  f"{h}%", font=font, fill=255)

                    draw.text((label_x, top+27),  "Pressure:", font=font, fill=255)
                    draw.text((value_x, top+27),  f"{p}hPa", font=font, fill=255)

                    draw.text((label_x, top+36),  "Door:", font=font, fill=255)
                    draw.text((value_x, top+36),  door_sensors, font=font, fill=255)

                    draw.text((label_x, top+45),  "Motion:", font=font, fill=255)
                    draw.text((value_x, top+45),  motion_sensors, font=font, fill=255)

                    draw.text((label_x, top+54),  "CpuTemp:", font=font, fill=255)
                    draw.text((value_x, top+54),  f"{cputemp}°C", font=font, fill=255)


                elif display_type == 'lcd_st7735':
                    now = datetime.datetime.now()

                    draw.text((x+35, top), 'R P i M S', font=font, fill="cyan")

                    draw.text((x, top+15), ' Temperature', font=font, fill="lime")
                    draw.text((x+77, top+15), f'{temperature} *C', font=font, fill="lime")

                    draw.text((x, top+28), ' Humidity', font=font, fill="lime")
                    draw.text((x+77, top+28), f'{humidity} %', font=font, fill="lime")

                    draw.text((x, top+41), ' Pressure', font=font, fill="lime")
                    draw.text((x+77, top+41), f'{pressure} hPa', font=font, fill="lime")

                    draw.text((x, top+57), ' Door', font=font, fill="yellow")
                    draw.text((x+77, top+57), door_sensors, font=font, fill="yellow")

                    draw.text((x, top+70), ' Motion', font=font, fill="yellow")
                    draw.text((x+77, top+70), motion_sensors, font=font, fill="yellow")

                    draw.text((x, top+86), ' CPUtemp', font=font, fill="cyan")
                    draw.text((x+77, top+86), f'{cputemp} *C', font=font, fill="cyan")

                    draw.text((x, top+99), ' IP', font=font, fill="cyan")
                    draw.text((x+36, top+99), hostip, font=font, fill="cyan")

                    draw.text((x+5, top+115), now.strftime("%Y-%m-%d %H:%M:%S"), font=font, fill="floralwhite")

            sleep(1 / refresh_rate)

    except Exception as err:
        logger.error(err)


def set_process_name_and_run(function_name, **kwargs):
    process_name = function_name.__name__
    setproctitle.setproctitle(process_name)
    function_name(**kwargs)


def threading_function(function_name, ctx):
    import threading
    tf = threading.Thread(
        target=function_name,
        name=function_name.__name__,
        args=(ctx,)
    )
    tf.daemon = True
    tf.start()


def multiprocessing_function(function_name, ctx):
    import multiprocessing
    mf = multiprocessing.Process(
        target=function_name,
        name=function_name.__name__,
        args=(ctx,)
    )
    mf.daemon = True
    mf.start()


def db_connect(dbhost, dbnum):
    try:
        redis_db = redis.StrictRedis(host=dbhost, port=6379, db=str(dbnum), decode_responses=True)
        redis_db.ping()
        return redis_db
    except Exception as err:
        logger.error(err)
        error = f"Can't connect to RedisDB host: {dbhost}"
        logger.error(error)
        sys.exit(1)


def config_load(path_to_config):
    try:
        with open(path_to_config, mode='r') as file:
            config_yaml = yaml.full_load(file)
        return config_yaml
    except Exception as err:
        logger.error(err)
        error = f"Can't load RPiMS config file: {path_to_config}"
        logger.error(error)
        sys.exit(1)


def main():
    logger.info('')
    logger.info('# RPiMS is running #')
    logger.info('')

    redis_db = db_connect('localhost', 0)
    config_yaml = config_load('../config/rpims.yaml')

    gpio = config_yaml.get("gpio")
    config = config_yaml.get("setup")
    zabbix_agent = config_yaml.get("zabbix_agent")
    sensors = config_yaml.get("sensors")

    ctx = AppContext(gpio, config, zabbix_agent, sensors, redis_db)

    redis_db.flushdb()
    redis_db.set('rpims', json.dumps(config_yaml))

    get_hostip()
    hostnamectl_sh(**ctx.zabbix_agent)

    if ctx.config.get('verbose'):
        for k, v in ctx.config.items():
            logger.info(f'{k} = {v}')
        for k, v in ctx.zabbix_agent.items():
            logger.info(f'{k} = {v}')
        logger.info('')

    # hardware initialization
    ctx.door_sensors = init_door_sensors(ctx)
    ctx.motion_sensors = init_motion_sensors(ctx)
    ctx.system_buttons = init_system_buttons(ctx)
    ctx.led_indicators = init_led_indicators(ctx)

    # door sensors – initial state + callbacks
    if ctx.config.get('use_door_sensor'):
        for name, sensor in ctx.door_sensors.items():
            if sensor.value == 0:
                door_status_open(ctx, name)
            else:
                door_status_close(ctx, name)

        for name, sensor in ctx.door_sensors.items():
            sensor.when_held = lambda s=name: door_action_closed(ctx, s)
            sensor.when_released = lambda s=name: door_action_opened(ctx, s)

        if ctx.config.get('use_door_led_indicator'):
            ctx.led_indicators['door_led'].source = all_values(*ctx.door_sensors.values())

    # motion sensors
    if ctx.config.get('use_motion_sensor'):
        for name, sensor in ctx.motion_sensors.items():
            if sensor.value == 0:
                motion_sensor_when_no_motion(ctx, name)
            else:
                motion_sensor_when_motion(ctx, name)

        for name, sensor in ctx.motion_sensors.items():
            sensor.when_motion = lambda s=name: motion_sensor_when_motion(ctx, s)
            sensor.when_no_motion = lambda s=name: motion_sensor_when_no_motion(ctx, s)

        if ctx.config.get('use_motion_led_indicator'):
            ctx.led_indicators['motion_led'].source = any_values(*ctx.motion_sensors.values())

    # system buttons
    if ctx.config.get('use_system_buttons'):
        ctx.system_buttons['shutdown_button'].when_held = shutdown

    # CPU temp
    if ctx.config.get('use_cpu_sensor'):
        threading_function(get_cputemp_data, ctx)

    # BME280
    if ctx.config.get('use_bme280_sensor'):
        for name, bme280 in ctx.bme280_config.items():
            if bme280.get('use'):
                sensor_ctx = SensorContext(ctx, name, bme280)
                multiprocessing_function(get_bme280_data, sensor_ctx)

    # DS18B20
    if ctx.config.get('use_ds18b20_sensor'):
        threading_function(get_ds18b20_data, ctx)

    # DHT
    if ctx.config.get('use_dht_sensor'):
        threading_function(get_dht_data, ctx)

    # Weather station
    if ctx.config.get('use_weather_station'):
        if ctx.rainfall_config.get('use'):
            threading_function(rainfall, ctx)
        if ctx.windspeed_config.get('use'):
            threading_function(wind_speed, ctx)
        if ctx.winddirection_config.get('use'):
            threading_function(wind_direction, ctx)

    # Serial display
    if ctx.config.get('use_serial_display'):
        threading_function(serial_displays, ctx)

    # Picamera
    if ctx.config.get('use_picamera'):
        av_stream('start')
    else:
        av_stream('stop')

    pause()


# --- Main program ---
if __name__ == '__main__':
    lock = acquire_lock()
    try:
        main()
    except KeyboardInterrupt:
        logger.info('# RPiMS is stopped #')
    except Exception as err:
        logger.error(err)
        sys.exit(1)
