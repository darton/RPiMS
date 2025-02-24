import machine
import bme280_float as bme280
from utime import sleep_ms


sid = 'BME280'

BME280VCC = machine.Pin(22, machine.Pin.OUT)
BME280VCC.value(1)
sleep_ms(1000)

SDA_PIN = machine.Pin(16)
SCL_PIN = machine.Pin(17)
SCL_FREQ = 100000
i2c = machine.I2C(0,sda=SDA_PIN, scl=SCL_PIN, freq=SCL_FREQ)

led = machine.Pin(25, machine.Pin.OUT)
led.value(0)


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

while True:
    try:
        val = bme.values
    except:
        print(' NODATA')
        reset_bme280()
        continue
    
    if len(val) == 3:
        t,h,p = int(float(val[0])*1000),int(float(val[2])*1000),int(float(val[1])*1000)
        print(sid,t,h,p)
        led_blinking(700,1300,1)
    else:
        print(' BADREAD')
        reset_bme280()

