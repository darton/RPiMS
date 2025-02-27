import utime
from utime import sleep_ms, sleep
import rp2
import machine
from machine import Pin, ADC
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

def read_ADC():
    adc = ADC(Pin(26))
    raw_value = adc.read_u16()  # Read the raw value from the ADC (0-65535)
    voltage = raw_value * 3.3 / 65535  # Scale to the voltage range (0-3.3V)
    battery_voltage = voltage * 2  # Account for the voltage divider
    return round(battery_voltage, 2)

def read_sensors():
    DHT22_VCC = Pin(22, Pin.OUT)
    DHT_DATA_PIN = Pin(20,Pin.IN,Pin.PULL_UP)
    utime.sleep_ms(1000)
    V = read_ADC()
    dht_sensor = DHT22(DHT_DATA_PIN,DHT22_VCC,dht11=False)
    T,H = dht_sensor.read()
    if T is not None and H <= 100:
        sensors_data = {
                        "temp": T,  # Temperature in °C
                        "hum": H,    # Humidity in %
                        "vcc": V # Battery voltage
                      }
        led_blinking(700,1300,1)
        return sensors_data
    else:
        print(' SENSOR ERROR')
        return None 


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
        cmd = f"HSET {REDIS_KEY} temperature {data['temp']} humidity {data['hum']} vcc {data['vcc']}"
        
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
        print(f"Data sent to Redis: {cmd}")
    except Exception as e:
        print("Error:", e)


def main():
    while True:
        # 1. Turn on Wi-Fi, read data, send to Redis
        connect_wifi()
        sensors_data = read_sensors()
        print (f"Data read from sensor: {sensors_data}")
        send_to_redis(sensors_data)
       
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

