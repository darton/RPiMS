import network
import socket
import machine
import urequests as requests
import ujson
import time
import bme280_float as bme280
from utime import sleep_ms
import sys
import rp2

# Konfiguracja
WIFI_SSID = "IoT"
WIFI_PASSWORD = "verycomplexwifipassword"

REDIS_HOST = "192.168.1.2"
REDIS_PORT = 6379
REDIS_PASSWORD = "verycomplexredispassword"
REDIS_KEY = "BME280PicoW01"

BME280VCC = machine.Pin(22, Pin.OUT)

led = machine.Pin("LED", machine.Pin.OUT)
led.off()

def led_blinking(on_time, off_time, number_of_blinks):
    for n in range(number_of_blinks):
        led.toggle()
        sleep_ms(on_time)
        led.toggle()
        sleep_ms(off_time)    
    

def reset_bme280():
    BME280VCC.value(0)
    led_blinking(150,350,2)
    BME280VCC.value(1)
    led_blinking(150,350,2)


def read_sensor():
    try:
        BME280VCC.value(1)
        sleep_ms(1000)
        SDA_PIN = machine.Pin(20)
        SCL_PIN = machine.Pin(21)
        SCL_FREQ = 100000
        i2c = machine.I2C(0,sda=SDA_PIN, scl=SCL_PIN, freq=SCL_FREQ)
        while True:
            try:
                BME280_I2CADDR = 0x76
                bme = bme280.BME280(i2c=i2c, address=BME280_I2CADDR)
                break
            except:
                try:
                    BME280_I2CADDR = 0x77
                    bme = bme280.BME280(i2c=i2c, address=BME280_I2CADDR)
                    break
                except Exception:
                    #reset_bme280()
                    pass
        val = bme.values
    except:
        print(' NODATA')
        #reset_bme280()
    
    if len(val) == 3:
        t,h,p = float(val[0]),float(val[2]),float(val[1])
        led_blinking(700,1300,2)
    else:
        print(' BADREAD')
        #reset_bme280()
    sensor_data = {
        "temp": t,  # Temperature in °C
        "pres": p,  # Pressure in hPa
        "hum": h    # Humidity in %
    }
    # Reset the I2C bus before entering lightsleep mode
    BME280VCC.value(0)
    return sensor_data


def connect_wifi():
    rp2.country('PL')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Connected to Wi-Fi, IP:", wlan.ifconfig()[0])

def send_to_redis(data):
    try:
        #data
        # Formatting data for Redis (e.g., HSET)
        cmd = f"HSET {REDIS_KEY} temperature {data['temp']} humidity {data['hum']} pressure {data['pres']}"
        
        # Establishing TCP connection with Redis
        addr = (REDIS_HOST, REDIS_PORT)
        s = socket.socket()
        s.connect(addr)
        
        # Authentication (if required)
        if REDIS_PASSWORD:
            s.send(f"AUTH {REDIS_PASSWORD}\r\n".encode())
            time.sleep(1)
        
        # Sending command
        s.send(f"{cmd}\r\n".encode())
        
        # Closing connection with Redis
        s.close()
        print("Data sent to Redis!")
    except Exception as e:
        print("Error:", e)


def main():
    while True:
        # 1. Turn on Wi-Fi, read data, send to Redis
        connect_wifi()
        sensor_data = read_sensor()
        print (f"Data read from sensor: {sensor_data}")
        send_to_redis(sensor_data)
        
        # 2. Turn off Wi-Fi and enter power-saving mode
        wlan = network.WLAN(network.STA_IF)
        wlan.disconnect()
        wlan.active(False)
        wlan.deinit()
        
        # 3. Put Pico to sleep for 60 seconds (light sleep)
        print("Sleeping...")
        machine.lightsleep(60 * 1000)  # 60,000 ms = 60 seconds

if __name__ == "__main__":
    main()

