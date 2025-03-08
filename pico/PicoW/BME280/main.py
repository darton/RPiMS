import network
import usocket as socket
import machine
import time
import bme280_float as bme280
from utime import sleep_ms, sleep
import rp2

# Configuration
WIFI_SSID = "IoT"
WIFI_PASSWORD = "verycomplexwifipassword"

REDIS_HOST = "192.168.1.2"
REDIS_PORT = 6379
REDIS_PASSWORD = "verycomplexredispassword"
REDIS_KEY = "BME280PicoW01"

BME280VCC = machine.Pin(22, machine.Pin.OUT)

MACHINE_SLEEP_TIME = 300 #seconds

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


def read_ADC():
    adc = machine.ADC(machine.Pin(28))
    raw_value = adc.read_u16()  # Read the raw value from the ADC (0-65535)
    voltage = raw_value * 3.3 / 65535  # Scale to the voltage range (0-3.3V)
    battery_voltage = voltage * 2  # Account for the voltage divider
    return round(battery_voltage, 2)


def read_sensors():
    sleep_ms(1000)
    v = read_ADC()
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
                    reset_bme280()
        val = bme.values  
        if len(val) == 3:
            t,h,p = float(val[0]),float(val[2]),float(val[1])
            sensor_data = {
            "temp": t,  # Temperature in °C
            "pres": p,  # Pressure in hPa
            "hum": h,    # Humidity in %
            "vcc": v # battery voltage
            }
            if t is not None and h is not None and p is not None:
                BME280VCC.value(0)
                led_blinking(700,1300,1)
                return sensor_data
            else:
                led_blinking(300,100,2)
                machine.reset()
    except:
        led_blinking(300,100,10)
        machine.reset()


def connect_wifi():
    rp2.country('PL')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    start_time = time.time()
    timeout = 60
    
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            if time.time() - start_time > timeout:
                machine.reset()
            led_blinking(100,100,5)

    print("Connected to Wi-Fi, IP:", wlan.ifconfig()[0])

def send_to_redis(data):
    try:
        #data
        # Formatting data for Redis (e.g., HSET)
        cmd = f"HSET {REDIS_KEY} temperature {data['temp']} humidity {data['hum']} pressure {data['pres']} vcc {data['vcc']}"
        cmde = f"EXPIRE {REDIS_KEY} {2 * MACHINE_SLEEP_TIME}"
        # Establishing TCP connection with Redis
        addr = (REDIS_HOST, REDIS_PORT)
        s = socket.socket()
        s.connect(addr)
        
        # Authentication (if required)
        if REDIS_PASSWORD:
            s.send(f"AUTH {REDIS_PASSWORD}\r\n".encode())
            sleep(1)
        # Sending commands
        for _cmd in (cmd, cmde):
            s.send(f"{_cmd}\r\n".encode())
            print(f"Data sent to Redis: {_cmd}")
            led_blinking(700,300,1)
        
        # Closing connection with Redis
        s.close()
        print("Data sent to Redis!")
        led_blinking(700,1300,1)
    except Exception as e:
        led_blinking(300,100,3)
        print("Error:", e)


def main():
    while True:
        # 1. Turn on Wi-Fi, read data, send to Redis
        connect_wifi()
        sensors_data = read_sensors()
        if sensors_data is not None:
            print (f"Data readed from sensor: {sensors_data}")
            send_to_redis(sensors_data)
        
        # 2. Turn off Wi-Fi and enter power-saving mode
        wlan = network.WLAN(network.STA_IF)
        wlan.disconnect()
        wlan.active(False)
        wlan.deinit()
        
        # 3. Put Pico to sleep for MACHINE_SLEEP_TIME seconds (light sleep)
        print("Sleeping...")
        machine.lightsleep(MACHINE_SLEEP_TIME * 1000)  # 60,000 ms = 60 seconds

if __name__ == "__main__":
    main()

