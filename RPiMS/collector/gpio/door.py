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

from gpiozero import Button
from gpiozero.tools import all_values

from gpio.helpers import (
    door_action_closed,
    door_action_opened,
    door_status_open,
    door_status_close
)

def init_door_sensors(ctx):
    sensors = {}
    if ctx.config.get('use_contact_sensor'):
        for name, cfg in ctx.gpio.items():
            if cfg['type'] == 'ContactSensor':
                sensors[name] = Button(cfg['pin'], hold_time=int(cfg['hold_time']))
    return sensors


def setup_door_callbacks(ctx):
    for name, sensor in ctx.door_sensors.items():
        if sensor.value == 0:
            door_status_open(ctx, name)
        else:
            door_status_close(ctx, name)

    for name, sensor in ctx.door_sensors.items():
        sensor.when_held = lambda s=name: door_action_closed(ctx, s)
        sensor.when_released = lambda s=name: door_action_opened(ctx, s)

    if ctx.config.get('use_contact_led_indicator'):
        ctx.led_indicators['door_led'].source = all_values(*ctx.door_sensors.values())
