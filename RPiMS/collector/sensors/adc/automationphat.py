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
from time import sleep
import automationhat

logger = logging.getLogger(__name__)

def adc_automationphat():
    sleep(0.1)  # Delay for automationhat
    return [automationhat.analog.one.read(), automationhat.analog.two.read(),
            automationhat.analog.three.read()]
