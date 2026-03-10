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

from gpiozero import LED

def init_led_indicators(ctx):
    leds = {}
    for name, cfg in ctx.gpio.items():
        if cfg['type'] == 'door_led':
            leds['door_led'] = LED(cfg['pin'])
        elif cfg['type'] == 'motion_led':
            leds['motion_led'] = LED(cfg['pin'])
        elif cfg['type'] == 'led':
            leds['led'] = LED(cfg['pin'])
    return leds

