RPi Monitoring System

When the door will opened or closed, a message is sent to the zabbix server. Then a 5-second video sequence is recorded, and then stream rtsp will run. 


sudo apt-get install python-gpiozero

sudo apt-get install vlc

sudo apt-get install  libav-tools

sudo apt-get install python-picamera

sudo apt-get install omxplayer

sudo apt-get -y remove fake-hwclock

sudo apt-get install zabbix-agent

sudo apt-get install build-essential python-dev

sudo apt-get install git-core

sudo apt-get install python3-gpiozero

sudo apt-get install -y gpac

sudo apt-get install fbi

sudo git clone https://github.com/adafruit/Adafruit_Python_DHT.git

mkdir /home/pi/scripts

mkdir /home/pi/video

cd /home/pi/scripts/


echo "UserParameter=dht.pull[*],sudo /home/pi/Adafruit_Python_DHT/examples/AdafruitDHT.py 11 17 | awk -F[=*%] '{print '$'"$1"}'" >>/etc/zabbix/zabbix_agentd.conf

echo "" > /etc/motd

echo "RPi Monitoring System" >> /etc/motd

echo "" >> /etc/motd


echo "echo" >> /home/pi/.bashrc

echo "/home/pi/scripts/dht11.py" >> /home/pi/.bashrc

echo "echo" >> /home/pi/.bashrc



#test only

sudo wget https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/dht11.py

raspivid -o test.h264

raspistill -o test.jpg

