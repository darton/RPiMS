#!/usr/bin/python3

import redis
from gpiozero import CPUTemperature

cpu = CPUTemperature()
#print('CPU temperature: {}C'.format(cpu.temperature))
redis_db.set('CPUtemperature', cpu.temperature)
