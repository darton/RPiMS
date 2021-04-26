from machine import Pin, I2C, reset
import bme280_float as bme280
#from utime import sleep, localtime, mktime, ticks_ms
from utime import sleep_ms#, ticks_ms
import sys

sid = 'BME280'

BME280VCC = Pin(22, Pin.OUT)
BME280VCC.value(1)
sleep_ms(1000)

SDA_PIN = machine.Pin(16)
SCL_PIN = machine.Pin(17)
SCL_FREQ = 100000
i2c = machine.I2C(0,sda=SDA_PIN, scl=SCL_PIN, freq=SCL_FREQ)

try:
    BME280_I2CADDR = 0x76
    bme = bme280.BME280(i2c=i2c, address=BME280_I2CADDR)
except:
    try:
        BME280_I2CADDR = 0x77
        bme = bme280.BME280(i2c=i2c, address=BME280_I2CADDR)
    except Exception:
        BME280VCC.value(0)
        sleep(1000)
        BME280VCC.value(1)
        sleep(1000)

while True:
    try:
        val = bme.values
    except:
        BME280VCC.value(0)
        sleep_ms(500)
        BME280VCC.value(1)
        sleep_ms(500)
        continue
    temp,hum,pres = int(float(val[0])*1000),int(float(val[2])*1000),int(float(val[1])*1000)
    sleep_ms (2000)
    print(sid,temp,hum,pres)
