# RPiMS

RPiMS is Raspberry Pi based Monitoring System (door sensor, temperature and humidity sensor, video streamer/recorder)

When the door will opened or closed, a trap message is sent to the zabbix server. 
Then a 5-second video sequence is recorded, and then stream rtsp will run. 


## Installing

```
sudo apt-get update

sudo apt-get install python3-gpiozero

sudo apt-get install python3-pip

sudo python3 -m pip install --upgrade pip setuptools wheel

sudo apt-get install build-essential python-dev

sudo apt-get install git-core

sudo apt-get install zabbix-agent


mkdir /home/pi/scripts

cd /home/pi/scripts/

git clone https://github.com/darton/RPi.git

echo "UserParameter=dht.pull[*],sudo /home/pi/scripts/RPi/ADHT.py | awk -F[=*%] '{print '$'"$1"}'" >>/etc/zabbix/zabbix_agentd.conf

echo 'Timeout=5' >> /etc/zabbix/zabbix_agentd.conf

Modify /etc/zabbix/zabbix_agentd.conf to Server= 127.0.0.1, zabbix.example.com

echo "" > /etc/motd

echo "RPi Monitoring System" >> /etc/motd

echo "" >> /etc/motd

echo "echo" >> /home/pi/.bashrc

echo "/home/pi/scripts/ADHT.py" >> /home/pi/.bashrc

echo "echo" >> /home/pi/.bashrc

sudo visudo 

```

### add below line 

```
zabbix ALL=(ALL) NOPASSWD: /home/pi/scripts/ADHT.py

```

### edit /etc/rc.local and add below line before command exit 0

```
su - pi -c '/home/pi/scripts/door-sensor.py &'
```

## If you have PiCamera

```
sudo apt-get install vlc

sudo apt-get install  libav-tools

sudo apt-get install python-picamera

sudo apt-get install omxplayer

sudo apt-get install -y gpac

sudo apt-get install fbi

mkdir /home/pi/video
```


## If you have RTC (DS3231 I2C)

```
sudo apt-get -y remove fake-hwclock

sudo rm /etc/cron.hourly/fake-hwclock

sudo update-rc.d -f fake-hwclock remove

sudo rm /etc/init.d/fake-hwclock

sudo update-rc.d hwclock.sh enable
```


## Test only

```
raspivid -o test.h264

raspistill -o test.jpg

sudo zabbix_get -s 127.0.0.1 -k dht.pull[4]

sudo zabbix_get -s 127.0.0.1 -k dht.pull[2]
```


## Usefull links

* [Raspberry Pi Documentaion](https://www.raspberrypi.org/documentation/hardware/raspberrypi/README.md)

* [Pinout](https://pinout.xyz/pinout/pin5_gpio3#)

* [GPIOZERO Docs](https://gpiozero.readthedocs.io/en/stable/)

* [HWclock tutorial](https://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi)


## Hardware setup - Raspberry Pi

 
 - Temperature and Humidity Sensor DHT11/DHT22
 
 BCM17 -> DOUT DHT11/DHT22
 

 - Hardware Clock
 
 3v3 Power     [pin 1] -> +

BCM2 (SDA)    [pin33] -> D

BCM3 (SCL)    [pin 5] -> C

BCM4 (GPCLK0) [pin 7] -> NC

Ground -> GND [pin 9] -> GND


- Input Sensors (door sensors)

Ground - > GND

BCM22 [pin 15] -> Input Sensor 1

BCM23 [pin 16] -> Input Sensor 2

BCM24 [pin 18] -> Input Sensor 3

BCM25 [pin 22] -> Input Sensor 4


