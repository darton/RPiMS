#!/usr/bin/env python3

import automationhat
from time import sleep

sleep(0.1)

count = 0
values = []

while True:
    value = round(automationhat.analog.one.read(),1)
    if not value in values:
        values.append(value)
        count+=1
        print(count,values)
