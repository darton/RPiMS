# RPiMS

RPiMS is Raspberry Pi based Monitoring System (door/window sensors, motion sensors, temperature, humidity, preassure sensors, video streamer/recorder from picamera)

## Description

The Zabbix Agent preriodicaly pull temperature and humidity data to Zabbix Server. 
When the door will opened or closed, a trap message is sent to the Zabbix server. 
Then a 5-second video sequence is recorded, and then stream rtsp will run. 

## Installing

### Installing operating system images 

Download the image [Raspbian Lite](https://downloads.raspberrypi.org/raspbian_lite_latest)

To writing an image to the SD card, use [Etcher](https://etcher.io/) an image writing tool.

If you're not using Etcher, you'll need to unzip .zip downloads to get the image file (.img) to write to your SD card.

### Run installation script
```
sudo curl -sS https://raw.githubusercontent.com/darton/RPiMS/master/install.sh |bash

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

## Install if you have PiCamera

```
sudo apt-get install -y vlc libav-tools omxplayer gpac fbi

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
sudo hwclock –r
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

Restart your Pi and check the I2C state again with `i2cdetect -y 1`. Now the 0x68 is not UU anymore. 
```
sudo sync
sudo reboot
```

## Test only

```
sudo apt-get install i2c-tools

i2cdetect -y 1

raspivid -o test.h264

raspistill -o test.jpg


sudo apt-get  install zabbix-proxy-sqlite

sudo zabbix_get -s 127.0.0.1 -k dht.pull[4]

sudo zabbix_get -s 127.0.0.1 -k dht.pull[2]
```

## Hardware setup - Raspberry Pi

 
 - Temperature and Humidity Sensor DHT11/DHT22
 
 BCM17 -> DOUT DHT11/DHT22/AM2302
 


 - Temperature, Humidity, Pressure Sensor BME280
 
 BCM2 [pin 3] - SDA
 
 BCM3 [pin 5] - SDC
 
 3v3 Power [pin 1] - VCC
 
 Ground [pin 9] - GND


- DS18B20 Temperature sensor

BCM4 [pin 7] -> D

3v3 Power [pin 1] - VCC

Ground [pin 9] - GND


 - Hardware Clock
 
 3v3 Power     [pin 1] -> +

BCM2 (SDA)    [pin33] -> D

BCM3 (SCL)    [pin 5] -> C

Ground -> GND [pin 9] -> GND



- Input Sensors (door sensors)

Ground - > GND

BCM22 [pin 15] -> Input Sensor 1 (Door/window sensor)

BCM23 [pin 16] -> Input Sensor 2 (Door/window sensor)

BCM12 [pin 32] -> Input Sensor 4 (Motion sensor)



- WaveShare HAT buttons

BCM21 [pin 40] -> Button 1

BCM20 [pin 38] -> Button 2

BCM16 [pin 36] -> Button 3



- WaveShare HAT Joystick

BCM5 [pin 29] -> Joytstick left

BCM6 [pin 31] -> Joytstick up

BCM13 [pin 33] -> Joytstick fire

BCM19 [pin 35] -> Joytstick down

BCM26 [pin 37] -> Joytstick right



## B.o.M - Bill of Materials

* BME280 or DHT11/DHT22/AM2302 or DS18B20 - 1 pcs
* Door/window Sensor - 2 pcs
* Motion Sensor - 1 pcs
* PiCamera - 1 pcs
* PiCamera Case - 1pcs
* Power Adapter (5V/2.5A) - 1 pcs
* Rapsberry Pi - 1 pcs
* Raspberri Pi Case - 1 pcs
* Waveshare OLED 1,3'' 128x64px SPI/I2C or Waveshare TFT 1,44'' 128x128px SPI - 1 pcs 
* ITALTRONIC 25.0410000.RP3 
* Male Headers 1x40 raster 2,54mm angle - 2 pcs
* RTC DS3231 I2C - 1 pcs


## Usefull links

* [Raspberry Pi Documentaion](https://www.raspberrypi.org/documentation/hardware/raspberrypi/README.md)

* [Pinout](https://pinout.xyz/pinout/pin5_gpio3#)

* [GPIOZERO Docs](https://gpiozero.readthedocs.io/en/stable/)

* [HWclock tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi)

* [BME280 Tutorial](https://pypi.org/project/RPi.bme280/)

* [DS18B20 Tutorial](https://github.com/timofurrer/w1thermsensor)

* [Luma Core](https://pypi.org/project/luma.core/)

* [TME Italtronic Case](https://www.tme.eu/pl/en/details/it-25.0410000.rp3/enclosure-for-embedded-systems/italtronic/25-0410000-rp3/)
* [TME Italtronic Case](https://www.tme.eu/pl/en/details/it-25.0610000.rp3/enclosure-for-embedded-systems/italtronic/25-0610000-rp3/)
* [Zabbix](https://zabbix.org/wiki/Main_Page)

* [WaveShare 1.3inch OLED HAT](https://www.waveshare.com/product/mini-pc/raspberry-pi/displays/1.3inch-oled-hat.htm)

* [WaveShare 1.44inch TFT HAT](https://www.waveshare.com/wiki/1.44inch_LCD_HAT)

* [Pi Camera](https://picamera.readthedocs.io/en/release-1.13/quickstart.html)

* [WaveShare Libraries for RPi](https://www.waveshare.com/wiki/Libraries_Installation_for_RPi)

* [RPi GPIO](https://elinux.org/RPi_BCM2835_GPIOs)

* [raspivid](https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspivid.md)
