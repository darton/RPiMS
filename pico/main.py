from machine import Pin, I2C
import bme280_float as bme280
from time import sleep

SDA_PIN = machine.Pin(16)
SCL_PIN = machine.Pin(17)
SCL_FREQ = 100000
i2c = machine.I2C(0,sda=SDA_PIN, scl=SCL_PIN, freq=SCL_FREQ)

BME280_I2CADDR = 0x77
bme = bme280.BME280(i2c=i2c, address=BME280_I2CADDR)

while True:
     val = bme.values
     temp,hum,pres = int(float(val[0])*1000), int(float(val[2])*1000),int(float(val[1])*1000)
     print(temp,hum,pres)
     sleep(2)
    
