# RPiMSv2

RPiMS is Raspberry Pi based Monitoring System 

Supports sensor like door/window sensor, motion sensor, water sensor, smoke sensor, light sensors.

Suppports I2C temperature, humidity, and preassure BME280 sensors, and 1-wire DS18B20 temperature sensors.

Supports UV4L Video Streaming Server and video recording from picamera.

Supports wind speed meter, wind direction meter, rainfall meter.


## Description

The Zabbix Agent periodicaly pull temperature,humidity and pressure sensor data from redis db and send to Zabbix Server. 

When any of the doors sensors opens or closed then a message will be sent to the Zabbix server. 

When the motion sensor detects motion a message will be sent to Zabbix server.

When any of the doors senors is opened, a video sequence will be recorded.

Video stream will be turned on automaticly when use picamera sensor are set to enable in setup.

Sensors are polled and measured values are saved to Redis database periodically. 


## Installing

### Installing operating system images 

Download the image [Raspberry Pi OS Lite](https://downloads.raspberrypi.org/raspios_lite_armhf_latest)

To writing an image to the SD card, use [Etcher](https://etcher.io/) an image writing tool or use [Imager](https://www.raspberrypi.org/downloads/)

If you're not using Etcher, you'll need to unzip .zip downloads to get the image file (.img) to write to your SD card.

### Run installation script

Running the following command will download and run the script.
```
sudo curl -sS https://raw.githubusercontent.com/darton/RPiMS/master/install.sh | bash

```

### Setup

login: admin

password: admin

```
http://rpiipaddress/setup
```

to change password type from CLI

```
htpasswd -b  /var/www/html/conf/.htpasswd admin newpassword
```

Start/Stop RPIMS
```
sudo systemctl start rpims.service
sudo systemclt stop rpims.service
```

### Main page

```
http://rpiipaddress
```

## Known issues
DHT22 sensor is not reliable. Required library libgpiod_pulsein may take 100% CPU or return bad reading or not return any readings, those are known bugs with issues in progress:
* [adafruit/Adafruit_Blinka: 100% CPU use of libgpiod_pulsein on Raspberry Pi](https://github.com/adafruit/Adafruit_CircuitPython_DHT/issues/50)


## Hardware setup - Raspberry Pi

 - ### Temperature, Humidity, Pressure Sensor BME280 - i2C on RPi
```
RPi  [VCC 3V3 Pin 1] ----------------------------- [VCC]  BME280
RPi   [GPIO.2 Pin 3] ----------------------------- [SDA]  BME280
RPi   [GPIO.3 Pin 5] ----------------------------- [SDC]  BME280
RPi    [GND - Pin 9] ----------------------------- [GND]  BME280
```

- ### Temperature, Humidity, Pressure Sensor BME280 - i2C on RPi Pico

If you want to use BME280 sensor on long cable, copy two files [main.py](https://raw.githubusercontent.com/darton/RPiMS/master/pico/main.py) and [bme280_float.py](https://raw.githubusercontent.com/darton/RPiMS/master/pico/bme280_float.py) from pico directory, to RPi Pico.

Connect the BME280 sensor to the i2C RPi Pico port:

```
RPi Pico  [GP22 Pin 29]------------------------------ [VCC]  BME280
RPi Pico  [GP16 Pin 21] ----------------------------- [SDA]  BME280
RPi Pico  [GP17 Pin 22] ----------------------------- [SDC]  BME280
RPi Pico  [GND  Pin 23] ----------------------------- [GND]  BME280
```


Connect the RPi with the RPi Pico together with the USB cable.

```
BME280 [i2c] <------> [i2C] RPi Pico [USB] <----------------------------------->  RPi [USB]
```

Select [USB port number](https://raw.githubusercontent.com/darton/RPiMS/master/documents/RPiMS-RPi-USB.png) in RPiMS configuration for the BME280 sensor.


- ### DS18B20 Temperature sensor
```
RPi   [VCC 3V3 Pin 1] -----------------------------  [VCC]    DS18B20
                                               |
                                               \
                                               /   R1 = 4k7
                                               \
                                               |
RPi  [GPIO.4 - Pin 7] ----------------------------- [DATA]   DS18B20


RPi     [GND - Pin 9] ----------------------------- [GND]    DS18B20
```

 - ### Temperature and Humidity Sensor DHT11/DHT22/AM2302 (NOT RECOMMENDED, UNSTABLE MEASUREMENTS)
```
RPi  [VCC 3V3 - Pin 1] -----------------------------  [VCC]    DHT22
                                               |
                                               \
                                               /   R1 = 4k7
                                               \
                                               |
RPi  [GPIO.17 - Pin 11] ----------------------------- [DATA]   DHT22


RPi      [GND - Pin 9] ----------------------------- [GND]    DHT22
```

I recommend using a level shifter and Vcc = 5V
```
RPi  [VCC 5V - Pin 2] --- [HV] - LEVEL SHIFTER --------------- [VCC]    DHT22
                                                         |
                                                          \
                                                          /   R1 = 4k7
                                                          \
                                                          |
RPi  [GPIO.17 - Pin 11] - [A1] - LEVEL SHIFTER - [B1]--------- [DATA]   DHT22
RPi  [VCC 3V3 - Pin 1] -- [LV] - LEVEL SHIFTER
RPi      [GND - Pin 9] ---[GND] - LEVEL SHIFTER -------------- [GND]    DHT22
```

 - ### OLED i2C Display
```
RPi  [VCC 3V3 pin 1] ----------------------------- [VCC]  OLED
RPi   [GPIO.2 pin 3] ----------------------------- [SDA]  OLED
RPi   [GPIO.3 pin 5] ----------------------------- [SDC]  OLED
RPi    [GND - pin 9] ----------------------------- [GND]  OLED
```

 - ### Hardware Clock
```
RPi  [VCC 3V3 pin 1] ----------------------------- [VCC]  DS3231
RPi   [GPIO.2 pin 3] ----------------------------- [SDA]  DS3231
RPi   [GPIO.3 pin 5] ----------------------------- [SDC]  DS3231
```

- Door/Window Sensors it is potential-free sensors like button.
- Motion Sensors it is digital sensors with binary output signal (3.3V).


## B.o.M - Bill of Materials

* BME280 - 1-3 pcs
* DS18B20 - 1 pcs or more (or DS18S20) 
* Resistor 4k7 (for DS18B20 sensor) - 1 psc
* DHT11/DHT22/AM2302 - 1 pcs 
* Door/window sensor - 1 or more pcs
* Motion Sensor - 1 or more pcs
* PiCamera - 1 pcs
* PiCamera Case - 1pcs
* Power Adapter (5V/2.5A or 5V1/3A for RPi4) - 1 pcs
* Rapsberry Pi - 1 pcs
* Raspberri Pi Case - 1 pcs
* Raspberry Pico - 1-3 pcs
* Sensor case for Pico and BME280 - 1-3 pcs
* RTC DS3231 I2C - 1 pcs
* LCD OLED 1,3" I2C SH1106 or 1.44" lcd_st7735 - 1 pcs
* Weather Meter Kit - 1 pcs
* ADC(STM32F030) or Pimoroni AutomationHat- 1pcs

Optional

* Waveshare OLED 1,3'' 128x64px SPI/I2C or Waveshare TFT 1,44'' 128x128px SPI - 1 pcs 
* ITALTRONIC 25.0410000.RP3 - 1 pcs
* Male Headers 1x40 raster 2,54mm angle - 2 pcs



## Usefull links

* [Raspberry Pi Documentaion](https://www.raspberrypi.org/documentation/hardware/raspberrypi/README.md)

* [Pinout](https://pinout.xyz/pinout/pin5_gpio3#)

* [Pinout](https://www.raspberrypi.org/documentation/usage/gpio/)

* [GPIOZERO Docs](https://gpiozero.readthedocs.io/en/stable/)

* [UV4L Tutorials](https://www.linux-projects.org/uv4l/tutorials/)

* [HWclock tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi)

* [BME280 Tutorial](https://pypi.org/project/RPi.bme280/)

* [DHT22](https://pypi.org/project/adafruit-circuitpython-dht/)

* [DS18B20 Tutorial](https://github.com/timofurrer/w1thermsensor)

* [Luma Core](https://pypi.org/project/luma.core/)

* [Frame buffer](https://wavesharejfs.blogspot.com/2018/03/raspberry-pi-driv-144inch-lcd-hat-with.html)

* [RPi 3B Case](https://www.tme.eu/pl/en/details/it-25.0410000.rp3/enclosure-for-embedded-systems/italtronic/25-0410000-rp3/)

* [RPi 4B Case](https://www.tme.eu/pl/en/details/it-25.0410000.rp4/enclosure-for-embedded-systems/italtronic/25-0410000-rp4/)

* [RPi Pico and BME280 Sensor Case](https://www.tme.eu/pl/en/details/pp73g/enclosures-for-alarms-and-sensors/supertronic/)

* [Sensor Case](https://pl.farnell.com/camdenboss/cbrs01vwh/enclosure-room-sensor-vented-white/dp/2472317?gclid=EAIaIQobChMIvvLvy47-5wIVQswYCh19AA4JEAQYAiABEgKsW_D_BwE&gross_price=true&mckv=Y1xp9UYm_dc|pcrid|155087520124|&CMP=KNC-GPL-GEN-SHOPPING-ALL_PRODUCTS)

* [Zabbix](https://zabbix.org/wiki/Main_Page)

* [Weather Meter Kit](https://learn.sparkfun.com/tutorials/weather-meter-hookup-guide?_ga=2.69275472.1527856563.1581318845-1560292620.1572271230)

* [WaveShare 1.3inch OLED HAT](https://www.waveshare.com/wiki/1.3inch_OLED_HAT)

* [WaveShare 1.44inch TFT HAT](https://www.waveshare.com/wiki/1.44inch_LCD_HAT)

* [Pi Camera](https://picamera.readthedocs.io/en/release-1.13/quickstart.html)

* [WaveShare Libraries for RPi](https://www.waveshare.com/wiki/Libraries_Installation_for_RPi)

* [RPi GPIO](https://elinux.org/RPi_BCM2835_GPIOs)

* [raspivid](https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md)

* [Color Names](https://www.w3schools.com/colors/colors_names.asp)

* [Configuring wifi in Linux with wpa_supplicant](https://shapeshed.com/linux-wifi/)

* [Raspberry Pi Zero OTG Mode](https://gist.github.com/gbaman/50b6cca61dd1c3f88f41)

* [RPi - Setting up a wireless LAN via the command line](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)

* [8-Channel 12-Bit ADC, Seeed Studio](https://pl.rs-online.com/web/p/products/1887099/)
 
* [Setup Camera with V4L2, FFMPEG, and PiCamera](https://www.codeinsideout.com/posts/raspberrypi/setup_camera/)

* [A Raspberry Pi Streaming Camera using MPEG-DASH, HLS or RTSP](https://codecalamity.com/a-raspberry-pi-streaming-camera-using-mpeg-dash-hls-or-rtsp/)


## Configure if you have RTC (DS3231 I2C)

1. I2C interface should be enabled. 

```
sudo raspi-config
```
Select Advaced Options -> I2C -> <Yes> 

2. Edit the configuration file to add a new device. 

```
sudo vi /boot/config.txt
```
Add a new RTC device DS3231 to the device tree 

```
dtoverlay=i2c-rtc,ds3231
```

Reboot to take effect. About Device Tree, see: `cat /boot/overlay/README` 

```
sudo reboot
```

3. Read the Hardware Clock. 
```
sudo hwclock -r
```
Read the system time: 
```
date
```
4. Set the Hardware Clock to the time given by the `--date` option. 
```
sudo hwclock --set --date="Aug-22-2019 08:29:00"
```
5. Set the System Time from the Hardware Clock. 
```
sudo hwclock -s
```
6. Read the RTC and system times. 
```
sudo hwclock -r; date
```
Remove fake-hwclock

```
sudo apt-get -y remove fake-hwclock

sudo update-rc.d -f fake-hwclock remove

sudo systemctl disable fake-hwclock 

sudo update-rc.d hwclock.sh enable

sudo nano /etc/rc.local
```

Add the following lines to the file: `/etc/rc.local`

```
sudo nano /etc/rc.local 
```
Add this commnads
```
sudo hwclock -s

date
```
Just before the `exit 0`

Restart your Pi and check the I2C state again with `i2cdetect -y 1` to the RTC address is not UU anymore. 
```
sudo sync
sudo reboot
```

## Configuration testing I2C devices

```
sudo apt-get install i2c-tools
```

Optionally, to improve permformance, increase the I2C baudrate from the default of 100KHz to 400KHz by altering /boot/config.txt to include:
```
dtparam=i2c_arm=on,i2c_baudrate=400000
```
Next check that the device is communicating properly.

```
$ i2cdetect -y 1
       0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
  00:          -- -- -- -- -- -- -- -- -- -- -- -- --
  10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  30: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
  40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
  70: -- -- -- -- -- -- 76 --
  ```

## Configuration testing picamera
```
raspivid -o test.h264

raspistill -o test.jpg

rtsp://rpiipaddress:8554/
```

## Configuration testing zabbix-agent
```
sudo apt-get  install zabbix-proxy-sqlite3

sudo zabbix_get -s 127.0.0.1 -k rpims.cputemp[2] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /var/www/html/conf/zabbix_agentd.conf)" --tls-psk-file=/var/www/html/conf/zabbix_agentd.psk


sudo zabbix_get -s 127.0.0.1 -k rpims.ds18b20[2] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /var/www/html/conf/zabbix_agentd.conf)" --tls-psk-file=/var/www/html/conf/zabbix_agentd.psk

sudo zabbix_get -s 127.0.0.1 -k rpims.ds18b20[4] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /var/www/html/conf/zabbix_agentd.conf)" --tls-psk-file=/var/www/html/conf/zabbix_agentd.psk


sudo zabbix_get -s 127.0.0.1 -k rpims.bme280[2] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /var/www/html/conf/zabbix_agentd.conf)" --tls-psk-file=/var/www/html/conf/zabbix_agentd.psk

sudo zabbix_get -s 127.0.0.1 -k rpims.bme280[4] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /var/www/html/conf/zabbix_agentd.conf)" --tls-psk-file=/var/www/html/conf/zabbix_agentd.psk

sudo zabbix_get -s 127.0.0.1 -k rpims.bme280[6] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /var/www/html/conf/zabbix_agentd.conf)" --tls-psk-file=/var/www/html/conf/zabbix_agentd.psk


sudo zabbix_get -s 127.0.0.1 -k rpims.dht[2] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /var/www/html/conf/zabbix_agentd.conf)" --tls-psk-file=/var/www/html/conf/zabbix_agentd.psk

sudo zabbix_get -s 127.0.0.1 -k rpims.dht[4] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /var/www/html/conf/zabbix_agentd.conf)" --tls-psk-file=/var/www/html/conf/zabbix_agentd.psk


zabbix_get -s 127.0.0.1 -k "system.cpu.load[all,avg1]" --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /var/www/html/conf/zabbix_agentd.conf)" --tls-psk-file=/var/www/html/conf/zabbix_agentd.psk
```
