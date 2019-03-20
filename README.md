RPi Video, Door, Temperature and Humidity Monitoring System

When the door will opened or closed, a message is sent to the zabbix server. Then a 5-second video sequence is recorded, and then stream rtsp will run. 


# TO INSTALL

sudo apt-get install python3-gpiozero

sudo apt-get install build-essential python-dev

sudo apt-get install git-core

sudo apt-get install zabbix-agent

mkdir /home/pi/scripts

cd /home/pi/scripts/

echo "UserParameter=dht.pull[*],sudo /home/pi/scripts/ADHT.py 11 17 | awk -F[=*%] '{print '$'"$1"}'" >>/etc/zabbix/zabbix_agentd.conf

echo 'Timeout=5' >> /etc/zabbix/zabbix_agentd.conf

echo "" > /etc/motd

echo "RPi Monitoring System" >> /etc/motd

echo "" >> /etc/motd


echo "echo" >> /home/pi/.bashrc

echo "/home/pi/scripts/dht11.py" >> /home/pi/.bashrc

echo "echo" >> /home/pi/.bashrc


sudo visudo 

# add below line 

zabbix ALL=(ALL) NOPASSWD: /home/pi/scripts/ADHT.py


# edit /etc/rc.local and add below line before command exit 0

su - pi -c '/home/pi/scripts/door-sensor.py &'


# If you have PiCamera

sudo apt-get install vlc

sudo apt-get install  libav-tools

sudo apt-get install python-picamera

sudo apt-get install omxplayer

sudo apt-get install -y gpac

sudo apt-get install fbi

mkdir /home/pi/video


# If you have hwclock

sudo apt-get -y remove fake-hwclock

sudo rm /etc/cron.hourly/fake-hwclock

sudo update-rc.d -f fake-hwclock remove

sudo rm /etc/init.d/fake-hwclock

sudo update-rc.d hwclock.sh enable



# Test only

raspivid -o test.h264

raspistill -o test.jpg

sudo zabbix_get -s 127.0.0.1 -k dht.pull[4]

sudo zabbix_get -s 127.0.0.1 -k dht.pull[2]


# Usefull links

https://pinout.xyz/pinout/pin5_gpio3#

https://gpiozero.readthedocs.io/en/stable/

https://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi

# Hardware setup

 - RPi pinout
 
 Thermal Sensor DHT11/DHT22
 
 BCM17 -> DOUT DHT11/DHT22

 - HWCLOCK
 3v3 Power     [pin 1] -> +

BCM2 (SDA)    [pin33] -> D

BCM3 (SCL)    [pin 5] -> C

BCM4 (GPCLK0) [pin 7] -> NC

Ground -> GND [pin 9] -> GND


- Door Sensors

Ground - > GND

BCM22 [pin 15] -> Door Sensor 1

BCM23 [pin 16] -> Door Sensor 2

BCM24 [pin 18] -> Door Sensor 3

BCM25 [pin 22] -> Door Sensor 4


