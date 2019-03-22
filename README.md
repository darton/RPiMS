# RPiMS

RPiMS is Raspberry Pi based Monitoring System (door sensor, temperature and humidity sensor, video streamer/recorder)

## Description

When the door will opened or closed, a trap message is sent to the Zabbix server. 
Then a 5-second video sequence is recorded, and then stream rtsp will run. 


## Installing

### Installing operating system images 

Download the image [Raspbian Lite](https://downloads.raspberrypi.org/raspbian_lite_latest)

To writing an image to the SD card, use [Etcher](https://etcher.io/) an image writing tool.

If you're not using Etcher, you'll need to unzip .zip downloads to get the image file (.img) to write to your SD card.

### Installing dependencies
```
sudo apt-get update

sudo apt-get install python3-gpiozero

sudo apt-get install python3-pip

sudo python3 -m pip install --upgrade pip setuptools wheel

sudo pip3 install Adafruit_DHT

sudo apt-get install build-essential python-dev

sudo apt-get install git-core

sudo apt-get install zabbix-agent
```

### Install from repository

```
mkdir /home/pi/scripts

cd /home/pi/scripts/

git clone https://github.com/darton/RPiMS.git
```

### Setup


Prepare zabbix agent

```
echo "UserParameter=dht.pull[*],sudo /home/pi/scripts/RPiMS/ADHT.py | awk -F[=*%] '{print '$'"$1"}'" >>/etc/zabbix/zabbix_agentd.conf

echo 'Timeout=5' >> /etc/zabbix/zabbix_agentd.conf

sudo nano /etc/zabbix/zabbix_agentd.conf 
```

Modify Server and ServerActive to:

```
Server=127.0.0.1, zabbix.example.com

ServerActive=zabbix.example.com
```

Run command

```
sudo visudo 

```

Add this line

```
zabbix ALL=(ALL) NOPASSWD: /home/pi/scripts/RPiMS/ADHT.py
```

Mofify MOTD and .bashhrc

```
echo "" > /etc/motd

echo "RPi Monitoring System" >> /etc/motd

echo "" >> /etc/motd

echo "echo" >> /home/pi/.bashrc

echo "/home/pi/scripts/ADHT.py" >> /home/pi/.bashrc

echo "echo" >> /home/pi/.bashrc
```

Prepare to run RPiMS scrip after restart

```
sudo nano /etc/rc.local
````

and add below line before command `exit 0`

```
su - pi -c '/home/pi/scripts/RPiMS/door-sensor.py &'
```

## Setup if you have PiCamera

```
sudo apt-get install vlc

sudo apt-get install libav-tools

sudo apt-get install python-picamera

sudo apt-get install omxplayer

sudo apt-get install -y gpac

sudo apt-get install fbi

mkdir /home/pi/video
```


## Setup if you have RTC (DS3231 I2C)

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
Reboot to take effect. About Device Tree, see: /boot/overlay/README 
3. Read the Hardware Clock. 
```
sudo hwclock –r
```
Read the system time: 
```
date
```
4. Set the Hardware Clock to the time given by the --date option. 
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

```
sudo nano /etc/rc.local
```-
Add the following lines to the file:

```
sudo hwclock -s

date
```
Just before the exit 0

Restart your Pi and check the I2C state again with i2cdetect -y 1. Now the 0x68 is not UU anymore. 
```
sudo sync
sudo reboot
```

## Test only

```
raspivid -o test.h264

raspistill -o test.jpg

sudo zabbix_get -s 127.0.0.1 -k dht.pull[4]

sudo zabbix_get -s 127.0.0.1 -k dht.pull[2]
```

## Hardware setup - Raspberry Pi

 
 - Temperature and Humidity Sensor DHT11/DHT22
 ```
 BCM17 -> DOUT DHT11/DHT22
 ```

 - Hardware Clock
 ```
 3v3 Power     [pin 1] -> +

BCM2 (SDA)    [pin33] -> D

BCM3 (SCL)    [pin 5] -> C

BCM4 (GPCLK0) [pin 7] -> NC

Ground -> GND [pin 9] -> GND
```

- Input Sensors (door sensors)
```
Ground - > GND

BCM22 [pin 15] -> Input Sensor 1

BCM23 [pin 16] -> Input Sensor 2

BCM24 [pin 18] -> Input Sensor 3

BCM25 [pin 22] -> Input Sensor 4
```

## B.o.M - Bill of Materials

* DHT22 - 1 pcs
* Door Sensor - 4 pcs
* PiCamera - 1 pcs
* PiCamera Case - 1pcs
* Power Adapter (5V/2.5A) - 1 pcs
* Rapsberry Pi - 1 pcs
* Raspberri Pi Case - 1 pcs
* RTC - 1 pcs


## Usefull links

* [Raspberry Pi Documentaion](https://www.raspberrypi.org/documentation/hardware/raspberrypi/README.md)

* [Pinout](https://pinout.xyz/pinout/pin5_gpio3#)

* [GPIOZERO Docs](https://gpiozero.readthedocs.io/en/stable/)

* [HWclock tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi)

