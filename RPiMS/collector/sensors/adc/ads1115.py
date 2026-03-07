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
import board
import busio
from adafruit_ads1x15 import ADS1115, AnalogIn, ads1x15

logger = logging.getLogger(__name__)

def adc_ads1115():

    # I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # ADC object
    ads = ADS1115(i2c)
    ads.gain = 1  # typical

    # Channels A0–A3
    chan0 = AnalogIn(ads, ads1x15.Pin.A0)
    chan1 = AnalogIn(ads, ads1x15.Pin.A1)
    chan2 = AnalogIn(ads, ads1x15.Pin.A2)
    chan3 = AnalogIn(ads, ads1x15.Pin.A3)

    return [
        chan0.voltage,
        chan1.voltage,
        chan2.voltage,
        chan3.voltage
    ]
