#!/usr/bin/python3

import redis
from gpiozero import CPUTemperature

cpu = CPUTemperature()
print('CPU temperature: {0:0.0f}C'.format(cpu.temperature))

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0, charset="utf-8", decode_responses=True)
redis_db.set('CPUtemperature', cpu.temperature)
