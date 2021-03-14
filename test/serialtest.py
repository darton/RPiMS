#!/usr/bin/env python3

import time
import serial
ser = serial.Serial(
 port='/dev/ttyACM0',
 baudrate = 38400,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=2
)

counter = 0
while counter < 10:
    x=ser.readline()
    print(x.decode('utf-8'))
    counter += 1
