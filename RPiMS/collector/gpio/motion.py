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

from gpiozero import MotionSensor
from gpiozero.tools import any_values

from gpio.helpers import (
    motion_sensor_when_motion,
    motion_sensor_when_no_motion
)

def init_motion_sensors(ctx):
    sensors = {}
    if ctx.config.get('use_digital_sensor'):
        for name, cfg in ctx.gpio.items():
            if cfg['type'] == 'DigitalSensor':
                sensors[name] = MotionSensor(cfg['pin'])
    return sensors


def setup_motion_callbacks(ctx):
    for name, sensor in ctx.motion_sensors.items():
        if sensor.value == 0:
            motion_sensor_when_no_motion(ctx, name)
        else:
            motion_sensor_when_motion(ctx, name)

    for name, sensor in ctx.motion_sensors.items():
        sensor.when_motion = lambda s=name: motion_sensor_when_motion(ctx, s)
        sensor.when_no_motion = lambda s=name: motion_sensor_when_no_motion(ctx, s)

    if ctx.config.get('use_digital_led_indicator'):
        ctx.led_indicators['motion_led'].source = any_values(*ctx.motion_sensors.values())
