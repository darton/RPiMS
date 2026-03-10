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

from gpio.door import init_door_sensors, setup_door_callbacks
from gpio.motion import init_motion_sensors, setup_motion_callbacks
from gpio.buttons import init_system_buttons, setup_system_buttons_callbacks
from gpio.leds import init_led_indicators

def init_hardware(ctx):
    if ctx.config.get('use_door_sensor'):
        ctx.door_sensors = init_door_sensors(ctx)
        setup_door_callbacks(ctx)

    if ctx.config.get('use_motion_sensor'):
        ctx.motion_sensors = init_motion_sensors(ctx)
        setup_motion_callbacks(ctx)

    if ctx.config.get('use_system_buttons'):
        ctx.system_buttons = init_system_buttons(ctx)
        setup_system_buttons_callbacks(ctx)

    if ctx.config.get('use_motion_led_indicator'):
        ctx.led_indicators = init_led_indicators(ctx)
