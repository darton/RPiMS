#!/usr/bin/env python

#Raspberry Pi script.
#Read status GPIO27 - PIN13


from time import sleep
import RPi.GPIO as GPIO
import os

button1=13
button1_status = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button1,GPIO.IN,pull_up_down=GPIO.PUD_UP)

if GPIO.input(button1)==1:
        button1_status = 1
        print ('The door is open')
else:
        print ('The door is closed')

while(1):
        if GPIO.input(button1)==1:
                if button1_status==0:
                        print ('The door has been opened')
                        button1_status = 1
                        sleep(.1)
        else:
                if button1_status==1:
                        print ('The door has been closed')
                        button1_status = 0
                        sleep(.1)
