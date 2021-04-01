from machine import Pin, I2C
import bme280_float as bme280
from time import sleep

SDA_PIN = machine.Pin(16)
SCL_PIN = machine.Pin(17)
SCL_FREQ = 100000
i2c = machine.I2C(0,sda=SDA_PIN, scl=SCL_PIN, freq=SCL_FREQ)

BME280_I2CADDR = 0x76
bme = bme280.BME280(i2c=i2c, address=BME280_I2CADDR)

m_id = machine.unique_id()
m_uid = '{:02x}{:02x}{:02x}{:02x}'.format(m_id[0], m_id[1], m_id[2], m_id[3])

while True:
     temp = int(float(bme.values[0])*1000)
     pres = int(float(bme.values[1])*1000)
     hum = int(float(bme.values[2])*1000)
     print(temp,hum,pres)
     #print(m_uid,temp,hum,pres)
     sleep(2)
    
