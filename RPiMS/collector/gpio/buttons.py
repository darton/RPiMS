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
from system.actions import shutdown


def init_system_buttons(ctx):
    buttons = {}
    if ctx.config.get('use_system_buttons'):
        for name, cfg in ctx.gpio.items():
            if cfg['type'] == 'ShutdownButton':
                buttons['shutdown_button'] = Button(cfg['pin'], hold_time=int(cfg['hold_time']))
    return buttons

def setup_system_buttons_callbacks(ctx):
    if ctx.config.get('use_system_buttons'):
        ctx.system_buttons['shutdown_button'].when_held = shutdown
