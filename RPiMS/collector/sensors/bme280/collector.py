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

import logging
import sys
from time import sleep
import subprocess
import smbus2
import bme280
import serial
from serial.serialutil import SerialException
import usb.core

logger = logging.getLogger(__name__)


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
                            "%s_BME280: Temperature: %.1f °C, Humidity: %.1f %%, Pressure: %.1f hPa",
                             sid,
                             temperature,
                             humidity,
                             pressure,
                             )

                    sleep(read_interval)

                except (KeyboardInterrupt, SystemExit):
                    break

                except Exception as err:
                    logger.info('Problem with sensor BME280: %s', err)
                    sleep(1)

        except Exception as err:
            logger.info('Problem initializing BME280 I2C: %s', err)
    # --- SERIAL MODE ---
    if interface_type == 'serial':
        def usb_power_cycle(delay=1):
            # USB power off
            subprocess.run(["sudo", "uhubctl", "-l", "1-1", "-a", "off"], check=True)
            sleep(delay)
            # USB power on
            subprocess.run(["sudo", "uhubctl", "-l", "1-1", "-a", "on"], check=True)

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
        except Exception as err:
            logger.error('Unknown serial device')
            logger.error(err)
            sys.exit(1)

        lecounter = 0
        necounter = 0

        # --- USB reset helper ---
        def reset_usbdevice():
            devices = usb.core.find(find_all=True)
            for item in devices:
                if hex(item.idVendor) == '0x2e8a':
                    item.reset()


        # --- USB power cycle helper ---
        def power_cycle_usbdevice(delay=1):
            # USB power off
            subprocess.run(["sudo", "uhubctl", "-l", "1-1", "-a", "off"], check=True)
            sleep(delay)
            # USB power on
            subprocess.run(["sudo", "uhubctl", "-l", "1-1", "-a", "on"], check=True)


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
                    logger.info("BME280PicoUSB not connected to port %s", usbport)
                    sleep(2)
                except Exception as err:
                    #logger.info("Resetting USB port for BME280PicoUSB on %s", usbport)
                    logger.error(err)
                    #reset_usbdevice()
                    logger.info("Power cycle on USB")
                    power_cycle_usbdevice(2)
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
                    logger.info("Could not open BME280PicoUSB on port %s", usbport)
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
                    logger.info("Lost connection with BME280PicoUSB on port %s", usbport)
                    find_serial_device(port, baudrate)
                    sleep(2)

        # --- main serial loop ---
        for line in serial_data(serial_port, 115200):
            msg = line.decode('utf-8').split()

            if len(msg) < 4:
                lecounter += 1
                redis_db.set('LECOUNTER', lecounter)
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
                        "%s_BME280: Temperature: %s°C, Humidity: %s%%, Pressure: %shPa",
                        sid,
                        temperature,
                        humidity,
                        pressure,
                    )

            else:
                necounter += 1
                redis_db.set('NECOUNTER', necounter)

            sleep(read_interval)
