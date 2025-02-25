import utime
from utime import sleep_ms, sleep
import rp2
import machine
from machine import Pin
import network
import usocket as socket
from PicoDHT import DHT22

# Configuration
WIFI_SSID = "IoT"
WIFI_PASSWORD = "verycomplexwifipassword"

REDIS_HOST = "192.168.1.2"
REDIS_PORT = 6379
REDIS_PASSWORD = "verycomplexredispassword"
REDIS_KEY = "DHT22PicoW01"

led = machine.Pin("LED", machine.Pin.OUT)
led.off()


def read_sensor():
    DHT22_VCC = Pin(22, Pin.OUT)
    DHT_DATA_PIN = Pin(20,Pin.IN,Pin.PULL_UP)
    utime.sleep_ms(1000)
    dht_sensor = DHT22(DHT_DATA_PIN,DHT22_VCC,dht11=False)
    T,H = dht_sensor.read()
    if T is not None and H <= 100:
        sensor_data = {
                        "temp": T,  # Temperature in °C
                        "hum": H    # Humidity in %
                      }
        print(sensor_data)
        led_blinking(700,1300,1)
        return sensor_data
    else:
        print(' SENSOR ERROR')


def led_blinking(on_time, off_time, number_of_blinks):
    for n in range(number_of_blinks):
        led.toggle()
        sleep_ms(on_time)
        led.toggle()
        sleep_ms(off_time)


def connect_wifi():
    rp2.country('PL')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            led_blinking(100,100,3)
    print("Connected to Wi-Fi, IP:", wlan.ifconfig()[0])

def send_to_redis(data):
    try:
        #data
        # Formatting data for Redis (e.g., HSET)
        cmd = f"HSET {REDIS_KEY} temperature {data['temp']} humidity {data['hum']}"
        
        # Establishing TCP connection with Redis
        addr = (REDIS_HOST, REDIS_PORT)
        s = socket.socket()
        s.connect(addr)
        
        # Authentication (if required)
        if REDIS_PASSWORD:
            s.send(f"AUTH {REDIS_PASSWORD}\r\n".encode())
            sleep(1)
        
        # Sending command
        s.send(f"{cmd}\r\n".encode())
        
        # Closing connection with Redis
        s.close()
        led_blinking(700,1300,1)
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
