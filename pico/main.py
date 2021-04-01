from machine import Pin, I2C
from time import sleep
import BME280

sda = Pin(16)
scl = Pin(17)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=100000)
BME280_i2c_address = 0x77

while True:
    bme = BME280.BME280(address=BME280_i2c_address,i2c=i2c)
    temp = int(float(bme.temperature)*1000)
    hum = int(float(bme.humidity)*1000)
    pres = int(float(bme.pressure)*1000)
    print(temp,hum,pres)
    sleep(1)
