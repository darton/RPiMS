from machine import Pin, I2C
from time import sleep
import BME280

sda=Pin(16)
scl=Pin(17)

i2c=machine.I2C(0,sda=sda, scl=scl, freq=400000)
while True:
    bme = BME280.BME280(i2c=i2c)
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure
    print(temp,hum,pres)
    sleep(1)

 
