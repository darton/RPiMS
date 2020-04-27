# RPiMS

RPiMS is Raspberry Pi based Monitoring System (door/window sensors, motion sensors, temperature, humidity, preassure sensors, video streamer/recorder from picamera)

## Description

The Zabbix Agent periodicaly pull temperature,humidity and pressure sensor data from redis db and send to Zabbix Server. 

When any of the doors opens or closed then a message will be sent to the Zabbix server. 

When the motion sensor detects motion a message will be sent to Zabbix server.

When any of the doors is opened, a 5 second video sequence will be recorded and the rtsp stream will be turned on.

When any of the motion sensors detect movement, the rtsp stream will be turned on.

When all of the doors are closed for more than 3 seconds and the motion sensors do not detect movement, rtsp stream will be turned off. 

Sensors are polled and measured values are saved to the database periodically. 

The default intervals: 

 * CPU temperature - 1 second

 * BME280 - 10 seconds

 * DS18B20 - 60 seconds
 
 * DHT22 - 10 seconds


## Installing

### Installing operating system images 

Download the image [Raspbian Lite](https://downloads.raspberrypi.org/raspbian_lite_latest)

To writing an image to the SD card, use [Etcher](https://etcher.io/) an image writing tool.

If you're not using Etcher, you'll need to unzip .zip downloads to get the image file (.img) to write to your SD card.

### Run installation script

Running the following command will download and run the script.
```
sudo curl -sS https://raw.githubusercontent.com/darton/RPiMS/master/install.sh | bash

```

### Setup

Prepare zabbix agent

```
sudo nano /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf 
```

Modify Server and ServerActive:

```
Server=127.0.0.1, zabbix.example.com

ServerActive=zabbix.example.com
```

Restart Zabbix service

```
sudo systemctl restart zabbix-agent.service
```

Start/Stop RPIMS
```
sudo systemctl start rpims.service
sudo systemclt stop rpims.service
```

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

rtsp://raspberrypi:8554/
```

## Configuration testing zabbix-agent
```
sudo apt-get  install zabbix-proxy-sqlite3

sudo zabbix_get -s 127.0.0.1 -k rpims.cputemp[2] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf)" --tls-psk-file=/etc/zabbix/zabbix_agentd.conf.d/zabbix_agentd.psk


sudo zabbix_get -s 127.0.0.1 -k rpims.ds18b20[2] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf)" --tls-psk-file=/etc/zabbix/zabbix_agentd.conf.d/zabbix_agentd.psk

sudo zabbix_get -s 127.0.0.1 -k rpims.ds18b20[4] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf)" --tls-psk-file=/etc/zabbix/zabbix_agentd.conf.d/zabbix_agentd.psk


sudo zabbix_get -s 127.0.0.1 -k rpims.bm280[2] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf)" --tls-psk-file=/etc/zabbix/zabbix_agentd.conf.d/zabbix_agentd.psk

sudo zabbix_get -s 127.0.0.1 -k rpims.bme280[4] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf)" --tls-psk-file=/etc/zabbix/zabbix_agentd.conf.d/zabbix_agentd.psk

sudo zabbix_get -s 127.0.0.1 -k rpims.bm280[6] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf)" --tls-psk-file=/etc/zabbix/zabbix_agentd.conf.d/zabbix_agentd.psk


sudo zabbix_get -s 127.0.0.1 -k rpims.dht22[2] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf)" --tls-psk-file=/etc/zabbix/zabbix_agentd.conf.d/zabbix_agentd.psk

sudo zabbix_get -s 127.0.0.1 -k rpims.dht22[4] --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf)" --tls-psk-file=/etc/zabbix/zabbix_agentd.conf.d/zabbix_agentd.psk



zabbix_get -s 127.0.0.1 -k "system.cpu.load[all,avg1]" --tls-connect=psk --tls-psk-identity="$(awk -F\= '/TLSPSKIdentity/ {print $2}' /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf)" --tls-psk-file=/etc/zabbix/zabbix_agentd.conf.d/zabbix_agentd.psk

```

## Hardware setup - Raspberry Pi

 - Temperature, Humidity, Pressure Sensor BME280
```
RPi  [VCC 3V3 Pin 1] ----------------------------- [VCC]  BME280
RPi   [GPIO.2 Pin 3] ----------------------------- [SDA]  BME280
RPi   [GPIO.3 Pin 5] ----------------------------- [SDC]  BME280
RPi    [GND - Pin 9] ----------------------------- [GND]  BME280
```

- DS18B20 Temperature sensor
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

 - Temperature and Humidity Sensor DHT11/DHT22/AM2302 (NOT RECOMMENDED, POOR QUALITY, UNSTABLE MEASUREMENTS)
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

 - OLED Display
```
RPi  [VCC 3V3 pin 1] ----------------------------- [VCC]  OLED
RPi   [GPIO.2 pin 3] ----------------------------- [SDA]  OLED
RPi   [GPIO.3 pin 5] ----------------------------- [SDC]  OLED
RPi    [GND - pin 9] ----------------------------- [GND]  OLED
```

 - Hardware Clock
```
RPi  [VCC 3V3 pin 1] ----------------------------- [VCC]  DS3231
RPi   [GPIO.2 pin 3] ----------------------------- [SDA]  DS3231
RPi   [GPIO.3 pin 5] ----------------------------- [SDC]  DS3231
```

- Input Sensors (door sensors)
```
RPi [GND - pin 9] -------- > GND to all Input Sensors
RPi [GPIO.22 - pin 15] ----> Input Sensor 1 (Door/window sensor)
RPi [GPIO.23 - pin 16] ----> Input Sensor 2 (Door/window sensor)
RPi [GPIO.18 - pin 12] ----> Input Sensor 3 (Motion sensor)
```

- Shudown button
```
RPi [GPIO.13 - pin 33] ------ [Button]
RPi [GND - pin 9] ----------- [Button]
```


## B.o.M - Bill of Materials

* BME280 - 1 pcs
* DS18B20 - 1 pcs or more (or DS18S20) 
* Resistor 4k7 (for DS18B20 sensor) - 1 psc
* DHT11/DHT22/AM2302 - 1 pcs (NOT RECOMMENDED, POOR QUALITY, UNSTABLE MEASUREMENTS)
* Door/window sensor - 1-2 pcs
* Motion Sensor - 1-5 pcs
* PiCamera - 1 pcs
* PiCamera Case - 1pcs
* Power Adapter (5V/2.5A or 5V1/3A for RPi4) - 1 pcs
* Rapsberry Pi - 1 pcs
* Raspberri Pi Case - 1 pcs
* RTC DS3231 I2C - 1 pcs
* LCD OLED 1,3" I2C SH1106 or 1.44" lcd_st7735 - 1 pcs

Optional

* Waveshare OLED 1,3'' 128x64px SPI/I2C or Waveshare TFT 1,44'' 128x128px SPI - 1 pcs 
* ITALTRONIC 25.0410000.RP3 - 1 pcs
* Male Headers 1x40 raster 2,54mm angle - 2 pcs



## Usefull links

* [Raspberry Pi Documentaion](https://www.raspberrypi.org/documentation/hardware/raspberrypi/README.md)

* [Pinout](https://pinout.xyz/pinout/pin5_gpio3#)

* [Pinout](https://www.raspberrypi.org/documentation/usage/gpio/)

* [GPIOZERO Docs](https://gpiozero.readthedocs.io/en/stable/)

* [HWclock tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi)

* [BME280 Tutorial](https://pypi.org/project/RPi.bme280/)

* [DHT22](https://pypi.org/project/adafruit-circuitpython-dht/)

* [DS18B20 Tutorial](https://github.com/timofurrer/w1thermsensor)

* [Luma Core](https://pypi.org/project/luma.core/)

* [Frame buffer](https://wavesharejfs.blogspot.com/2018/03/raspberry-pi-driv-144inch-lcd-hat-with.html)

* [RPi Case](https://www.tme.eu/pl/en/details/it-25.0410000.rp3/enclosure-for-embedded-systems/italtronic/25-0410000-rp3/)

* [RPi Case](https://www.tme.eu/pl/en/details/it-25.0610000.rp3/enclosure-for-embedded-systems/italtronic/25-0610000-rp3/)

* [Sensor Case](https://www.tme.eu/pl/details/it-61.6020000/obudowy-urzadzen-alarmowych-i-czujnikow/italtronic/61-6020000/)

* [Sensor Case](https://pl.farnell.com/camdenboss/cbrs01vwh/enclosure-room-sensor-vented-white/dp/2472317?gclid=EAIaIQobChMIvvLvy47-5wIVQswYCh19AA4JEAQYAiABEgKsW_D_BwE&gross_price=true&mckv=Y1xp9UYm_dc|pcrid|155087520124|&CMP=KNC-GPL-GEN-SHOPPING-ALL_PRODUCTS)
* [Zabbix](https://zabbix.org/wiki/Main_Page)

* [WaveShare 1.3inch OLED HAT](https://www.waveshare.com/product/mini-pc/raspberry-pi/displays/1.3inch-oled-hat.htm)

* [WaveShare 1.44inch TFT HAT](https://www.waveshare.com/wiki/1.44inch_LCD_HAT)

* [Pi Camera](https://picamera.readthedocs.io/en/release-1.13/quickstart.html)

* [WaveShare Libraries for RPi](https://www.waveshare.com/wiki/Libraries_Installation_for_RPi)

* [RPi GPIO](https://elinux.org/RPi_BCM2835_GPIOs)

* [raspivid](https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md)

* [Color Names](https://www.w3schools.com/colors/colors_names.asp)

