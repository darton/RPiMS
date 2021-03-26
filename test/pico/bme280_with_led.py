from _thread import start_new_thread
from sys import stdin, exit
from machine import Pin, PWM, I2C
from time import sleep
import BME280

terminateThread = False
sda = Pin(16)
scl = Pin(17)

i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
BME280_i2c_address = 0x77

def blink_led():
    from time import sleep
    pwm = PWM(Pin(25))
    pwm.freq(1000)
    global terminateThread
    
    while True:
        if terminateThread:
            break
        for duty in range(65025):
            pwm.duty_u16(duty)
            sleep(0.0001)
        for duty in range(65025, 0, -1):
            pwm.duty_u16(duty)
            sleep(0.0001)

start_new_thread(blink_led, ())

try:
    while True:
        bme = BME280.BME280(address=BME280_i2c_address,i2c=i2c)
        temp = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
        print(temp,hum,pres)
        sleep(1)
except KeyboardInterrupt:                   # trap Ctrl-C input
    terminateThread = True                  # signal second 'background' thread to terminate 
    exit()
