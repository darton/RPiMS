from machine import Pin, I2C
import bme280_float as bme280
from time import sleep

sda_pin = Pin(16)
scl_pin = Pin(17)
i2c = I2C(0,sda=sda_pin, scl=scl_pin, freq=100000)

BME280_I2CADDR = 0x76
#i2c = machine.I2C(0)
bme = bme280.BME280(i2c=i2c, address=BME280_I2CADDR)

while True:
     temp = int(float(bme.values[0])*1000)
     pres = int(float(bme.values[1])*1000)
     hum = int(float(bme.values[2])*1000)
     print(temp,hum,pres)
     sleep(1)
