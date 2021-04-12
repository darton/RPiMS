from machine import Pin, I2C, reset
import bme280_float as bme280
from utime import sleep_ms
import sys

uid = 'BME280SN003'

sleep_ms(1000)

SDA_PIN = machine.Pin(16)
SCL_PIN = machine.Pin(17)
SCL_FREQ = 400000
i2c = machine.I2C(0,sda=SDA_PIN, scl=SCL_PIN, freq=SCL_FREQ)

try:
    BME280_I2CADDR = 0x76
    bme = bme280.BME280(i2c=i2c, address=BME280_I2CADDR)
except:
    try:
        BME280_I2CADDR = 0x77
        bme = bme280.BME280(i2c=i2c, address=BME280_I2CADDR)
    except Exception as e:
        machine.reset()

while True:
    try:
        val = bme.values
    except:
        sleep_ms(1000)
        try:
            val = bme.values
        except:
            macine.reset()
    temp,hum,pres = int(float(val[0])*1000),int(float(val[2])*1000),int(float(val[1])*1000)
    print(temp,hum,pres,uid)
    sleep_ms (2000)
