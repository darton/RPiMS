RPi Video, Door, Temperature and Humidity Monitoring System

When the door will opened or closed, a message is sent to the zabbix server. Then a 5-second video sequence is recorded, and then stream rtsp will run. 

https://pinout.xyz/pinout/pin5_gpio3#

https://gpiozero.readthedocs.io/en/stable/

###TO INSTALL###

sudo apt-get install python3-gpiozero

sudo apt-get install build-essential python-dev

sudo apt-get install git-core

sudo apt-get install zabbix-agent

mkdir /home/pi/scripts

cd /home/pi/scripts/

echo "UserParameter=dht.pull[*],sudo /home/pi/scripts/ADHT.py 11 17 | awk -F[=*%] '{print '$'"$1"}'" >>/etc/zabbix/zabbix_agentd.conf

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



#to test only

raspivid -o test.h264

raspistill -o test.jpg

sudo zabbix_get -s 127.0.0.1 -k dht.pull[4]

sudo zabbix_get -s 127.0.0.1 -k dht.pull[2]

