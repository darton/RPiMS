#!/usr/bin/env python3

# -*- coding:utf-8 -*-
#
#  Author : Dariusz Kowalczyk
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License Version 2 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

# --- Functions ---

def door_action_closed(door_id, **kwargs):
    lconfig = dict(kwargs)
    redis_db.set(str(door_id), 'close')
    if bool(kwargs['verbose']) is True:
        print(f'The {door_id} has been closed!')
    if bool(kwargs['use_zabbix_sender']) is True:
        zabbix_sender_call('info_when_door_has_been_closed', door_id)
    if bool(kwargs['use_picamera']) is True:
        if detect_no_alarms(**lconfig):
            av_stream('stop')


def door_action_opened(door_id, **kwargs):
    redis_db.set(str(door_id), 'open')
    if bool(kwargs['verbose']) is True:
        print(f'The {door_id} has been opened!')
    if bool(kwargs['use_zabbix_sender']) is True:
        zabbix_sender_call('info_when_door_has_been_opened', door_id)
    if bool(kwargs['use_picamera']) is True:
        if bool(kwargs['use_picamera_recording']) is True:
            av_stream('stop')
            av_recording()
        av_stream('start')


def door_status_open(door_id, **kwargs):
    redis_db.set(str(door_id), 'open')
    if bool(kwargs['verbose']) is True:
        print(f'The {door_id} is opened!')
    if bool(kwargs['use_zabbix_sender']) is True:
        zabbix_sender_call('info_when_door_is_opened', door_id)
    if bool(kwargs['use_picamera']) is True:
        av_stream('start')


def door_status_close(door_id, **kwargs):
    lconfig = dict(kwargs)
    redis_db.set(str(door_id), 'close')
    if bool(kwargs['verbose']) is True:
        print(f'The {door_id} is closed!')
    if bool(kwargs['use_zabbix_sender']) is True:
        zabbix_sender_call('info_when_door_is_closed', door_id)
    if bool(kwargs['use_picamera']) is True:
        if detect_no_alarms(**lconfig):
            av_stream('stop')


def motion_sensor_when_motion(ms_id, **kwargs):
    redis_db.set(str(ms_id), 'motion')
    if bool(kwargs['verbose']) is True:
        print(f'The {ms_id} : motion was detected!')
    if bool(kwargs['use_zabbix_sender']) is True:
        zabbix_sender_call('info_when_motion', ms_id)
    if bool(kwargs['use_picamera']) is True:
        av_stream('start')


def motion_sensor_when_no_motion(ms_id, **kwargs):
    lconfig = dict(kwargs)
    redis_db.set(str(ms_id), 'nomotion')
    if bool(kwargs['verbose']) is True:
        print(f'The {ms_id} : no motion')
    if bool(kwargs['use_picamera']) is True:
        if detect_no_alarms(**lconfig):
            av_stream('stop')


def detect_no_alarms(**kwargs):
    if bool(kwargs['use_door_sensor']) is True and bool(kwargs['use_motion_sensor']) is True:
        door_sensor_values = []
        motion_sensor_values = []
        for s in door_sensors_list:
            door_sensor_values.append(door_sensors_list[s].value)
        for s in motion_sensors_list:
            motion_sensor_values.append(int(not motion_sensors_list[s].value))
        if all(door_sensor_values) and all(motion_sensor_values):
            return True
    if bool(kwargs['use_door_sensor']) is True and bool(kwargs['use_motion_sensor']) is False:
        door_sensor_values = []
        for s in door_sensors_list:
            door_sensor_values.append(door_sensors_list[s].value)
        if all(door_sensor_values):
            return True
    if bool(kwargs['use_door_sensor']) is False and bool(kwargs['use_motion_sensor']) is True:
        motion_sensor_values = []
        for s in motion_sensors_list:
            motion_sensor_values.append(int(not motion_sensors_list[s].value))
        if all(motion_sensor_values):
            return True


def av_stream(state):
    from subprocess import call
    _cmd = '/home/pi/scripts/RPiMS/videostreamer.sh' + " " + state
    call(_cmd, shell=True)


def av_recording():
    from subprocess import call
    _cmd = '/home/pi/scripts/RPiMS/videorecorder.sh'
    call(_cmd, shell=True)


def zabbix_sender_call(message, sensor_id):
    from subprocess import call
    _cmd = '/home/pi/scripts/RPiMS/zabbix_sender.sh ' + message + " " + str(sensor_id)
    call(_cmd, shell=True)


def hostnamectl_sh(**kwargs):
    from subprocess import call
    hctldict = {"location": "set-location", "chassis": "set-chassis", "deployment": "set-deployment", }
    _cmd = 'sudo raspi-config nonint do_hostname' + ' "' + kwargs['hostname'] + '"'
    call(_cmd, shell=True)
    for item in hctldict:
        _cmd = 'sudo /usr/bin/hostnamectl ' + hctldict[item] + ' "' + kwargs[item] + '"'
        call(_cmd, shell=True)


def get_hostip():
    from subprocess import call
    _cmd = '/home/pi/scripts/RPiMS/gethostinfo.sh'
    call(_cmd, shell=True)


def shutdown():
    from subprocess import check_call
    check_call(['sudo', 'poweroff'])


def get_cputemp_data(**kwargs):
    verbose = kwargs['verbose']
    read_interval = kwargs['CPUtemp_read_interval']
    try:
        from time import sleep
        from gpiozero import CPUTemperature
        while True:
            data = CPUTemperature()
            redis_db.set('CPU_Temperature', data.temperature)
            redis_db.expire('CPU_Temperature', read_interval*2)
            if bool(verbose) is True:
                print('CPU temperature: {0:0.1f}'.format(data.temperature), chr(176)+'C', sep='')
                print('')
            sleep(read_interval)
    except Exception as err:
        print(f'Problem with CPU sensor: {err}')


def get_bme280_data(**kwargs):
    from time import sleep
    verbose = kwargs['verbose']
    read_interval = kwargs['BME280_read_interval']
    interface_type = kwargs['BME280_interface']

    if interface_type == 'i2c':
        try:
            import smbus2
            import bme280
            port = 1
            address = kwargs['BME280_i2c_address']
            bus = smbus2.SMBus(port)
            calibration_params = bme280.load_calibration_params(bus, address)
            while True:
                data = bme280.sample(bus, address, calibration_params)
                redis_db.mset({'BME280_Humidity': round(data.humidity,3), 'BME280_Temperature': round(data.temperature,3), 'BME280_Pressure': round(data.pressure,3)})
                redis_db.expire('BME280_Temperature', read_interval*2)
                redis_db.expire('BME280_Humidity', read_interval*2)
                redis_db.expire('BME280_Pressure', read_interval*2)
                if bool(verbose) is True:
                    print('')
                    print('BME280 Temperature: {0:0.1f}\xb0C'.format(data.temperature))
                    print('BME280 Humidity: {0:0.0f}%'.format(data.humidity))
                    print('BME280 Pressure: {0:0.0f}hPa'.format(data.pressure))
                    print('')
                sleep(read_interval)
        except Exception as err:
            print(f'Problem with sensor BME280: {err}')

    if interface_type == 'serial':
        lecounter = 0
        necounter = 0
        def serial_data(port, baudrate, timeout):
            import serial
            ser = serial.Serial(port, baudrate, timeout)
            while True:
                yield ser.readline()

        for line in serial_data('/dev/ttyACM0', 115200, 5):
            msg = line.decode('utf-8').split()
            if len(msg)< 3:
                lecounter += 1
                redis_db.set('LECOUNTER', lecounter)
                continue
            if msg[0].isnumeric() and msg[1].isnumeric() and msg[2].isnumeric():
                temperature = int(msg[0])/1000
                humidity = int(msg[1])/1000
                pressure = int(msg[2])/1000
                redis_db.mset({'BME280_Temperature': temperature, 'BME280_Humidity': humidity, 'BME280_Pressure': pressure})
                redis_db.expire('BME280_Temperature', read_interval*2)
                redis_db.expire('BME280_Humidity', read_interval*2)
                redis_db.expire('BME280_Pressure', read_interval*2)
                if bool(verbose) is True:
                    print(f'BME280 on serial: Temperature: {temperature}°C, Humidity: {humidity}%, Pressure: {pressure}hPa')
            else:
                necounter += 1
                redis_db.set('NECOUNTER', necounter)
            sleep(0.1)


def get_ds18b20_data(**kwargs):
    verbose = kwargs['verbose']
    read_interval = kwargs['DS18B20_read_interval']
    try:
        from w1thermsensor import W1ThermSensor
        from time import sleep
        while True:
            data = W1ThermSensor.get_available_sensors([W1ThermSensor.THERM_SENSOR_DS18B20, W1ThermSensor.THERM_SENSOR_DS18S20])
            for sensor in data:
                redis_db.sadd('DS18B20_sensors', sensor.id)
                redis_db.set(sensor.id, sensor.get_temperature())
                sleep(1)
                redis_db.expire(sensor.id, read_interval*2)
                if bool(verbose) is True:
                    print("Sensor %s temperature %.2f" % (sensor.id, sensor.get_temperature()), "\xb0C")
                    print('')
            redis_db.expire('DS18B20_sensors', read_interval*2)
            sleep(read_interval)
    except Exception as err:
        print(f'Problem with sensor DS18B20: {err}')


def get_dht_data(**kwargs):
    verbose = kwargs['verbose']
    read_interval = kwargs['DHT_read_interval']
    dht_type = kwargs['DHT_type']
    pin = kwargs['DHT_pin']
    import adafruit_dht
    from time import sleep

    debug = "yes"
    delay = 0
    dht_device = adafruit_dht.DHT22(pin)
    if dht_type == "DHT11":
        dht_device = adafruit_dht.DHT11(pin)

    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            redis_db.mset({'DHT_Humidity': humidity, 'DHT_Temperature': temperature, })
            redis_db.expire('DHT_Humidity', read_interval*2)
            redis_db.expire('DHT_Temperature', read_interval*2)
            if bool(verbose) is True:
                print(dht_type + " Temperature: {:.1f}°C ".format(temperature))
                print(dht_type + " Humidity: {}% ".format(humidity))
                print('')
            delay -= 1
            if delay < 0:
                delay = 0
        except OverflowError as error:
            if debug is 'yes':
                print(f'Problem with DHT sensor: {error}')
            delay += 1
        except  RuntimeError as error:
            if debug is 'yes':
                print(f'Problem with DHT sensor - {error}')
            delay += 1
        finally:
            if debug is 'yes':
                print(f'DHT delay: {delay}')
            redis_db.set('DHT_delay', delay)
            sleep(read_interval+delay)


def serial_displays(**kwargs):

    if kwargs['serial_display_type'] == 'oled_sh1106':
        from luma.core.interface.serial import i2c, spi
        from luma.core.render import canvas
        # from luma.core import lib
        from luma.oled.device import sh1106
        # from PIL import Image
        # from PIL import ImageDraw
        from PIL import ImageFont
        from time import sleep
        import logging
        # import socket

        # Load default font.
        font = ImageFont.load_default()
        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        width = 128
        height = 64
        # image = Image.new('1', (width, height))
        # First define some constants to allow easy resizing of shapes.
        padding = 0
        top = padding
        bottom = height-padding
        display_rotate = kwargs['serial_display_rotate']
        # Move left to right keeping track of the current x position for drawing shapes.
        x = 0

        logging.basicConfig(filename='/tmp/rpims_serial_display.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
        logger = logging.getLogger(__name__)

        serial_type = kwargs['serial_type']

        #if serial_type == 'i2c':
        serial = i2c(port=1, address=0x3c)
        if serial_type == 'spi':
            serial = spi(device=0, port=0, bus_speed_hz=8000000, transfer_size=4096, gpio_DC=24, gpio_RST=25)

        try:
            device = sh1106(serial, rotate=display_rotate)
            while True:
                with canvas(device) as draw:
                    # get data from redis db
                    values = redis_db.mget('BME280_Temperature', 'BME280_Humidity', 'BME280_Pressure', 'GPIO_5', 'GPIO_6', 'CPU_Temperature', 'hostip')

                    t,h,p = values[0], values[1], values[2]
                    if t == None or h == None or p == None:
                        temperature = '--.--'
                        humidity = '--.--'
                        pressure = '--.--'
                    elif t.replace('.','',1).isdigit() and h.replace('.','',1).isdigit() and p.replace('.','',1).isdigit():
                        temperature = round(float(t), 1)
                        humidity = int(round(float(h), 1))
                        pressure = int(round(float(p), 1))

                    door_sensor_1, door_sensor_2  = values[3], values[4]
                    if door_sensor_1 == None or door_sensor_2 == None:
                        door_sensor_1 = '-----'
                        door_sensor_2 = '-----'

                    cputemp = values[5]
                    if cputemp == None:
                        cputemp = '-----'
                    else:
                        cputemp = round(float(cputemp), 1)
                    hostip = values[6]
                    if hostip == None:
                        hostip = '---.---.---.---'

                    # draw on oled
                    draw.text((x, top),       'IP:' + str(hostip), font=font, fill=255)
                    draw.text((x, top+9),     f'Temperature..{temperature}°C', font=font, fill=255)
                    draw.text((x, top+18),    f'Humidity.....{humidity}%',  font=font, fill=255)
                    draw.text((x, top+27),    f'Pressure.....{pressure}hPa',  font=font, fill=255)
                    draw.text((x, top+36),    f'Door 1.......{door_sensor_1}',  font=font, fill=255)
                    draw.text((x, top+45),    f'Door 2.......{door_sensor_2}',  font=font, fill=255)
                    draw.text((x, top+54),    f'CpuTemp......{cputemp}°C', font=font, fill=255)
                sleep(1/kwargs['serial_display_refresh_rate'])
        except Exception as err:
            logger.error(err)

    if kwargs['serial_display_type'] == 'lcd_st7735':
        from luma.core.interface.serial import spi
        from luma.core.render import canvas
        # from luma.core import lib
        from luma.lcd.device import st7735
        # from PIL import Image
        # from PIL import ImageDraw
        from PIL import ImageFont
        # from PIL import ImageColor
        # import RPi.GPIO as GPIO
        from time import time, sleep
        import datetime
        import logging
        # import socket
        import redis
    # Load default font.
        font = ImageFont.load_default()
    # Display width/height
        width = 128
        height = 128
    # First define some constants to allow easy resizing of shapes.
        padding = 0
        top = padding
        # bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
        x = 0

        logging.basicConfig(filename='/tmp/rpims_serial_display.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
        logger = logging.getLogger(__name__)
        display_rotate = kwargs['serial_display_rotate']
        serial = spi(device=0, port=0, bus_speed_hz=8000000, transfer_size=4096, gpio_DC=25, gpio_RST=27)

        try:
            device = st7735(serial)
            device = st7735(serial, width=128, height=128, h_offset=1, v_offset=2, bgr=True, persist=False, rotate=display_rotate)

            while True:
                # get data from redis db
                values = redis_db.mget('BME280_Temperature', 'BME280_Humidity', 'BME280_Pressure', 'GPIO_5', 'GPIO_6', 'CPU_Temperature', 'hostip')

                t,h,p = values[0], values[1], values[2]
                if t == None or h == None or p == None:
                    temperature = '--.--'
                    humidity = '--.--'
                    pressure = '--.--'
                elif t.replace('.','',1).isdigit() and h.replace('.','',1).isdigit() and p.replace('.','',1).isdigit():
                    temperature = round(float(t), 1)
                    humidity = int(round(float(h), 1))
                    pressure = int(round(float(p), 1))

                door_sensor_1, door_sensor_2  = values[3], values[4]
                if door_sensor_1 == None or door_sensor_2 == None:
                    door_sensor_1 = '-----'
                    door_sensor_2 = '-----'

                cputemp = values[5]
                if cputemp == None:
                    cputemp = '-----'
                else:
                    cputemp = round(float(cputemp), 1)

                hostip = values[6]
                if hostip == None:
                    hostip = '---.---.---.---'

                now = datetime.datetime.now()
                # Draw
                with canvas(device) as draw:
                    draw.text((x+35, top), 'R P i M S', font=font, fill="cyan")
                    draw.text((x, top+15), ' Temperature', font=font, fill="lime")
                    # draw.text((x+71, top+15),'', font=font, fill="blue")
                    draw.text((x+77, top+15), str(temperature) + ' *C', font=font, fill="lime")

                    draw.text((x, top+28), ' Humidity',  font=font, fill="lime")
                    # draw.text((x+70, top+28),'', font=font, fill="blue")
                    draw.text((x+77, top+28), str(humidity) + ' %',  font=font, fill="lime")

                    draw.text((x, top+41), ' Pressure',  font=font, fill="lime")
                    # draw.text((x+70, top+41),'', font=font, fill="blue")
                    draw.text((x+77, top+41), str(pressure) + ' hPa',  font=font, fill="lime")

                    draw.text((x, top+57), ' Door 1',  font=font, fill="yellow")
                    # draw.text((x+70, top+57),'', font=font, fill="yellow")
                    draw.text((x+77, top+57), str(door_sensor_1),  font=font, fill="yellow")

                    draw.text((x, top+70), ' Door 2',  font=font, fill="yellow")
                    # draw.text((x+70, top+70),'', font=font, fill="yellow")
                    draw.text((x+77, top+70), str(door_sensor_2),  font=font, fill="yellow")

                    draw.text((x, top+86), ' CPUtemp',  font=font, fill="cyan")
                    draw.text((x+77, top+86), str(cputemp) + " *C",  font=font, fill="cyan")

                    draw.text((x, top+99), ' IP', font=font, fill="cyan")
                    draw.text((x+17, top+99), ':', font=font, fill="cyan")
                    draw.text((x+36, top+99), str(hostip), font=font, fill="cyan")

                    draw.text((x+5, top+115), now.strftime("%Y-%m-%d %H:%M:%S"),  font=font, fill="floralwhite")

                sleep(1/kwargs['serial_display_refresh_rate'])
        except Exception as err:
            logger.error(err)


def rainfall(**kwargs):
    from time import time, sleep
    from gpiozero import Button
    import math

    def bucket_tipped():
        nonlocal bucket_counter
        bucket_counter += 1

    def reset_bucket_counter():
        nonlocal bucket_counter
        bucket_counter = 0

    def calculate_rainfall():
        # global BUCKET_SIZE
        rainfall = round(bucket_counter * BUCKET_SIZE, 0)
        return rainfall

    rain_sensor = Button(kwargs['rainfall_sensor_pin'])
    rain_sensor.when_pressed = bucket_tipped

    bucket_counter = 0
    rainfall_acquisition_time = kwargs['rainfall_acquisition_time']
    rainfall_agregation_time = kwargs['rainfall_agregation_time']
    rainfalls = []

    # global BUCKET_SIZE
    BUCKET_SIZE = 0.2794  # [mm]

    while True:
        start_time = time()
        while time() - start_time <= rainfall_acquisition_time:
            reset_bucket_counter()
            sleep(rainfall_acquisition_time)
            # rainfall = calculate_rainfall()
            if len(rainfalls) == (rainfall_agregation_time/rainfall_acquisition_time):
                rainfalls.clear()
            rainfalls.append(calculate_rainfall())
        daily_rainfall = round(math.fsum(rainfalls), 1)
        if bool(kwargs['verbose']) is True:
            print(f'Rainfall: {rainfall}mm, Daily rainfall: {daily_rainfall}mm')
        redis_db.mset({'daily_rainfall': daily_rainfall, 'rainfall': rainfall})


def wind_speed(**kwargs):
    import statistics
    from gpiozero import Button
    from time import time, sleep

    def anemometer_pulse_counter():
        nonlocal anemometer_pulse
        anemometer_pulse += 1

    def reset_anemometer_pulse_counter():
        nonlocal anemometer_pulse
        anemometer_pulse = 0

    def calculate_speed(wind_speed_acquisition_time):
        nonlocal anemometer_pulse
        rotations = anemometer_pulse/2
        wind_speed_km_per_hour = round(ANEMOMETER_FACTOR * rotations * 2.4/wind_speed_acquisition_time, 1)
        return wind_speed_km_per_hour

    wind_speed_sensor = Button(kwargs['windspeed_sensor_pin'])
    wind_speed_sensor.when_pressed = anemometer_pulse_counter

    anemometer_pulse = 0
    wind_speed_acquisition_time = kwargs['windspeed_acquisition_time']
    wind_speed_agregation_time = kwargs['windspeed_agregation_time']
    wind_speeds = []
    average_wind_speeds = []
    daily_wind_gusts = []
    ANEMOMETER_FACTOR = 1.18

    while True:
        start_time = time()
        while time() - start_time <= wind_speed_acquisition_time:
            reset_anemometer_pulse_counter()
            sleep(wind_speed_acquisition_time)
            # wind_speed = calculate_speed(wind_speed_acquisition_time)
            if len(wind_speeds) == (wind_speed_agregation_time/wind_speed_acquisition_time):
                del wind_speeds[0]
            wind_speeds.append(calculate_speed(wind_speed_acquisition_time))
        wind_gust = max(wind_speeds)
        if len(daily_wind_gusts) == (86400/wind_speed_acquisition_time):
            del daily_wind_gusts[0]
        daily_wind_gusts.append(wind_gust)
        daily_wind_gust = max(daily_wind_gusts)

        average_wind_speed = round(statistics.mean(wind_speeds), 1)
        if len(average_wind_speeds) == (86400/wind_speed_agregation_time):
            del average_wind_speeds[0]
        average_wind_speeds.append(average_wind_speed)
        daily_average_wind_speed = round(statistics.mean(average_wind_speeds), 1)

        if bool(kwargs['verbose']) is True:
            print(f'Wind speed:{wind_speed}km/h, Wind gust:{wind_gust}km/h, Daily wind gust:{daily_wind_gust}km/h, Average wind speed:{average_wind_speed}km/h, Daily average wind speed:{daily_average_wind_speed}km/h')
        redis_db.mset({'wind_speed': wind_speed, 'wind_gust': wind_gust, 'daily_wind_gust': daily_wind_gust, 'average_wind_speed': average_wind_speed, 'daily_average_wind_speed': daily_average_wind_speed})


def adc_stm32f030():
    from grove.i2c import Bus

    ADC_DEFAULT_IIC_ADDR = 0X04
    ADC_CHAN_NUM = 8

    REG_RAW_DATA_START = 0X10
    REG_VOL_START = 0X20
    REG_RTO_START = 0X30

    REG_SET_ADDR = 0XC0

    class Pi_hat_adc():
        def __init__(self, bus_num=1, addr=ADC_DEFAULT_IIC_ADDR):
            self.bus=Bus(bus_num)
            self.addr=addr

        def get_all_vol_milli_data(self):
            array = []
            for i in range(ADC_CHAN_NUM):
                data = self.bus.read_i2c_block_data(self.addr, REG_VOL_START+i, 2)
                val = data[1] << 8 | data[0]
                array.append(val)
            return array

        def get_nchan_vol_milli_data(self, n):
            data = self.bus.read_i2c_block_data(self.addr, REG_VOL_START+n, 2)
            val = data[1] << 8 | data[0]
            return val

    adc = Pi_hat_adc()
    adc_inputs_values = adc.get_all_vol_milli_data()
    return adc_inputs_values


def adc_automationphat():
    import automationhat
    from time import sleep
    sleep(0.1)  # Delay for automationhat
    adc_inputs_values = [automationhat.analog.one.read(), automationhat.analog.two.read(),
                         automationhat.analog.three.read()]
    return adc_inputs_values


def adc_ads1115():
    import board
    import busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the ADC object using the I2C bus
    ads = ADS.ADS1115(i2c)
    chan1 = AnalogIn(ads, ADS.P0)
    chan2 = AnalogIn(ads, ADS.P1)
    chan3 = AnalogIn(ads, ADS.P2)
    chan4 = AnalogIn(ads, ADS.P3)
    adc_inputs_values = [chan1.voltage, chan2.voltage, chan3.voltage, chan4.voltage]
    return adc_inputs_values


def wind_direction(**kwargs):
    from time import time
    import math

    def get_average(angles):
        sin_sum = 0.0
        cos_sum = 0.0

        for angle in angles:
            r = math.radians(angle)
            sin_sum += math.sin(r)
            cos_sum += math.cos(r)

        flen = float(len(angles))
        s = sin_sum / flen
        c = cos_sum / flen
        arc = math.degrees(math.atan(s / c))
        average = 0.0

        if s > 0 and c > 0:
            average = arc
        elif c < 0:
            average = arc + 180
        elif s < 0 < c:
            average = arc + 360

        return 0.0 if average == 360 else average

    direction_mapr = {
        "N": 5080,
        "NNE": 5188,
        "NE": 6417,
        "ENE": 6253,
        "E": 17419,
        "ESE": 9380,
        "SE": 11613,
        "SSE": 6968,
        "S": 8129,
        "SSW": 5419,
        "SW": 5542,
        "W": 4781,
        "NW": 4977,
        "NNW": 4877,
        }

    direction_mapa = {
        "N": 0,
        "NNE": 22.5,
        "NE": 45,
        "ENE": 67.5,
        "E": 90,
        "ESE": 112.5,
        "SE": 135,
        "SSE": 157.5,
        "S": 180,
        "SSW": 202.5,
        "SW": 225,
        "W": 270,
        "NW": 315,
        "NNW": 337.5
        }

    uin = 5.2
    uout = 0
    r1 = 4690
    r2 = 0
    wind_direction_acquisition_time = kwargs['winddirection_acquisition_time']
    angles = []
    average_wind_direction = 0

    while True:
        start_time = time()
        angles.clear()
        while time() - start_time <= wind_direction_acquisition_time:
            if kwargs['winddirection_adc_type'] == 'AutomationPhat':
                adc_values = adc_automationphat()
            if kwargs['winddirection_adc_type'] == 'STM32F030':
                adc_values = adc_stm32f030()
            if kwargs['winddirection_adc_type'] == 'ADS1115':
                adc_values = adc_ads1115()

            if kwargs['winddirection_adc_input'] == 1:
                uout = round(adc_values[0], 1)
            if kwargs['winddirection_adc_input'] == 2:
                uout = round(adc_values[1], 1)
            if kwargs['winddirection_adc_input'] == 3:
                uout = round(adc_values[2], 1)
            if kwargs['winddirection_adc_input'] == 4:
                uout = round(adc_values[3], 1)

            if kwargs['reference_voltage_adc_input'] == 1:
                uin = round(adc_values[0], 1)
            if kwargs['reference_voltage_adc_input'] == 2:
                uin = round(adc_values[1], 1)
            if kwargs['reference_voltage_adc_input'] == 3:
                uin = round(adc_values[2], 1)
            if kwargs['reference_voltage_adc_input'] == 4:
                uin = round(adc_values[3], 1)

            if uin != uout and uin != 0:
                r2 = int(r1/(1 - uout/uin))
                # print(r2,uin,uout)
            else:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                print(f'Uin = {uin}')
                print(f'Uout = {uout}')
                print('Check sensor connections to ADC')
                print('Wind Direction Meter program was terminated')
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                quit()
            for item in direction_mapr:
                if (r2 <= direction_mapr.get(item) * 1.005) and (r2 >= direction_mapr.get(item) * 0.995):
                    angles.append(direction_mapa.get(item))
        if len(angles) != 0:
            average_wind_direction = int(round(get_average(angles), 0))
            if bool(kwargs['verbose']) is True:
                print(f'Average Wind Direction: {average_wind_direction}')
            redis_db.mset({'average_wind_direction': average_wind_direction, 'wind_direction': item})


def threading_function(function_name, **kwargs):
    import threading
    t = threading.Thread(target=function_name, name=function_name, kwargs=kwargs)
    t.daemon = True
    t.start()


def multiprocessing_function(function_name, **kwargs):
    import multiprocessing
    p = multiprocessing.Process(target=function_name, name=function_name, kwargs=kwargs)
    p.start()


def db_connect(dbhost, dbnum):
    import redis
    import sys
    from systemd import journal

    try:
        redis_db = redis.StrictRedis(host=dbhost, port=6379, db=str(dbnum), charset="utf-8", decode_responses=True)
        redis_db.ping()
        return redis_db
    except:
        error = f"Can't connect to RedisDB host: {dbhost}"
        journal.send(error)
        sys.exit(error)


def config_load(path_to_config):
    import sys
    from systemd import journal

    try:
        import yaml
        with open(path_to_config, mode='r') as file:
            config_yaml = yaml.full_load(file)
        return config_yaml
    except:
        error = f"Can't load RPiMS config file: {path_to_config}"
        journal.send(error)
        sys.exit(error)


def use_logger():
    import logging
    logging.basicConfig(filename='/tmp/rpims.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    global logger
    logger = logging.getLogger(__name__)


def main():
    # from picamera import PiCamera
    from gpiozero import LED, Button, MotionSensor
    from gpiozero.tools import all_values, any_values
    from signal import pause
    # import logging
    import json
    import sys

    print('')
    print('# RPiMS is running #')
    print('')

    global redis_db
    redis_db = db_connect('localhost', 0)

    config_yaml = config_load('/var/www/html/conf/rpims.yaml')
    config = config_yaml['setup']
    zabbix_agent = config_yaml['zabbix_agent']
    gpio = config_yaml.get("gpio")

    redis_db.flushdb()
    redis_db.set('gpio', json.dumps(gpio))
    redis_db.set('config', json.dumps(config))
    redis_db.set('zabbix_agent', json.dumps(zabbix_agent))

    get_hostip()
    hostnamectl_sh(**zabbix_agent)

    if bool(config['verbose']) is True:
        for k, v in config.items():
            print(f'{k} = {v}')
        for k, v in zabbix_agent.items():
            print(f'{k} = {v}')
        print('')

    if bool(config['use_door_sensor']) is True:
        global door_sensors_list
        door_sensors_list = {}
        for item in gpio:
            if (gpio[item]['type'] == 'DoorSensor'):
                door_sensors_list[item] = Button(gpio[item]['gpio_pin'], hold_time=int(gpio[item]['hold_time']))

    if bool(config['use_motion_sensor']) is True:
        global motion_sensors_list
        motion_sensors_list = {}
        for item in gpio:
            if (gpio[item]['type'] == 'MotionSensor'):
                motion_sensors_list[item] = MotionSensor(gpio[item]['gpio_pin'])

    if bool(config['use_system_buttons']) is True:
        global system_buttons_list
        system_buttons_list = {}
        for item in gpio:
            if (gpio[item]['type'] == 'ShutdownButton'):
                system_buttons_list['shutdown_button'] = Button(gpio[item]['gpio_pin'], hold_time=int(gpio[item]['hold_time']))

    global led_indicators_list
    led_indicators_list = {}
    for item in gpio:
        if (gpio[item]['type'] == 'door_led'):
            led_indicators_list['door_led'] = LED(gpio[item]['gpio_pin'])
        if (gpio[item]['type'] == 'motion_led'):
            led_indicators_list['motion_led'] = LED(gpio[item]['gpio_pin'])
        if (gpio[item]['type'] == 'led'):
            led_indicators_list['led'] = LED(gpio[item]['gpio_pin'])

    if bool(config['use_door_sensor']) is True:
        for k, v in door_sensors_list.items():
            if v.value == 0:
                door_status_open(k, **config)
            else:
                door_status_close(k, **config)
        for k, v in door_sensors_list.items():
            v.when_held = lambda s=k: door_action_closed(s, **config)
            v.when_released = lambda s=k: door_action_opened(s, **config)
        if bool(config['use_door_led_indicator']) is True:
            led_indicators_list['door_led'].source = all_values(*door_sensors_list.values())

    if bool(config['use_motion_sensor']) is True:
        for k, v in motion_sensors_list.items():
            if v.value == 0:
                motion_sensor_when_no_motion(k, **config)
            else:
                motion_sensor_when_motion(k, **config)
        for k, v in motion_sensors_list.items():
            v.when_motion = lambda s=k: motion_sensor_when_motion(s, **config)
            v.when_no_motion = lambda s=k: motion_sensor_when_no_motion(s, **config)
        if bool(config['use_motion_led_indicator']) is True:
            led_indicators_list['motion_led'].source = any_values(*motion_sensors_list.values())

    if bool(config['use_system_buttons']) is True:
        system_buttons_list['shutdown_button'].when_held = shutdown

    if bool(config['use_CPU_sensor']) is True:
        threading_function(get_cputemp_data, **config)

    if bool(config['use_BME280_sensor']) is True:
        threading_function(get_bme280_data, **config)

    if bool(config['use_DS18B20_sensor']) is True:
        threading_function(get_ds18b20_data, **config)

    if bool(config['use_DHT_sensor']) is True:
        threading_function(get_dht_data, **config)

    if bool(config['use_weather_station']) is True:
        threading_function(rainfall, **config)
        threading_function(wind_speed, **config)
        threading_function(wind_direction, **config)

    if bool(config['use_serial_display']) is True:
        threading_function(serial_displays, **config)

    if bool(config['use_picamera']) is True and bool(config['use_picamera_recording']) is False and bool(config['use_door_sensor']) is False and bool(config['use_motion_sensor']) is False:
        av_stream('start')

    pause()


# --- Main program ---
if __name__ == '__main__':
    from pid import PidFile
    try:
        with PidFile('/home/pi/scripts/RPiMS/rpims.pid'):
            main()
    except KeyboardInterrupt:
        print('')
        print('# RPiMS is stopped #')
    except Exception as err :
        print(f'Another instance of RPiMS is already running. RPiMS will now close. {err}')
