from machine import Pin
from PicoDHT import DHT22
from utime import sleep_ms

sleep_ms(1000)
sid = 'BME280'

DHT22_VCC = Pin(22, Pin.OUT)
DHT_DATA_PIN = Pin(20,Pin.IN,Pin.PULL_UP)

dht_sensor = DHT22(DHT_DATA_PIN,DHT22_VCC,dht11=False)

while True:
    T,H = dht_sensor.read()
    if T is not None and H <= 100:
        t,h = (int(float(T)*1000),int(float(H)*1000))
        print(sid,t,h,999999)
    else:
        print(' SENSOR ERROR')
    sleep_ms(1000)
