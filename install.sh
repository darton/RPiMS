#!/bin/bash

echo "Do you want to install the RPiMS software?"
read -r -p "$1 [y/N] " response < /dev/tty
if [[ $response =~ ^(yes|y|Y)$ ]]; then
    echo "Greats ! The installation has started."
else
    echo "OK. Exiting"
    exit
fi

sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_onewire 0
sudo raspi-config nonint do_camera 0
#raspi-config nonint do_serial 1
sudo raspi-config nonint do_change_timezone Europe/Warsaw

installdir=/home/pi/scripts/RPiMS
wwwdir=/var/www/html

[[ -d $wwwdir ]] || sudo mkdir -p $wwwdir
[[ -d $wwwdir/conf ]] || sudo mkdir -p $wwwdir/conf
[[ -d $wwwdir/css ]] || sudo mkdir -p $wwwdir/css
[[ -d $wwwdir/setup ]] || sudo mkdir -p $wwwdir/setup
[[ -d $wwwdir/stream ]] || sudo mkdir -p $wwwdir/stream
[[ -d $installdir ]] || mkdir -p $installdir
[[ -d /home/pi/Videos ]] || mkdir -p /home/pi/Videos

for file in $(curl -sS https://raw.githubusercontent.com/darton/RPiMS/RPiMSv2/files.txt); do
   curl -sS https://raw.githubusercontent.com/darton/RPiMS/RPiMSv2/$file -o $installdir/$file
done

curl -sS https://www.w3schools.com/w3css/4/w3.css -o $installdir/w3.css
curl -sS https://www.w3schools.com/lib/w3-colors-2020.css -o $installdir/w3-colors-2020.css
curl -sS https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js -o $installdir/jquery.min.js
curl -sS https://cdn.jsdelivr.net/npm/hls.js@latest/dist/hls.min.js.map -o $installdir/hls.min.js.map
curl -sS https://cdn.jsdelivr.net/npm/hls.js@latest/dist/hls.min.js -o $installdir/hls.min.js
curl -sS https://cdn.jsdelivr.net/npm/hls.js@latest -o $installdir/hls.js

chmod u+x $installdir/*.py $installdir/*.sh

sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get autoremove
sudo apt-get -y install python3-gpiozero python3-pip build-essential python3-dev python3-numpy python3-picamera python3-w1thermsensor python3-automationhat python3-systemd
sudo apt-get -y install git libfreetype6-dev libopenjp2-7 libtiff5 libjpeg-dev vlc ffmpeg gpac fbi

sudo python3 -m pip install --upgrade pip setuptools wheel
sudo -H pip3 install --upgrade RPi.bme280 redis pid PyYAML luma.oled luma.lcd adafruit-circuitpython-ads1x15 rshell pyusb

sudo apt-get -y install redis-server
sudo systemctl enable redis-server.service
sudo sysctl -w vm.overcommit_memory=1
sudo sysctl -w net.core.somaxconn=512
echo 'vm.overcommit_memory=1' | sudo tee -a /etc/sysctl.conf
echo 'net.core.somaxconn=512' | sudo tee -a /etc/sysctl.conf
echo 'maxmemory 100mb' | sudo tee -a /etc/redis/redis.conf
sudo systemctl start redis-server.service

sudo apt-get -y install nginx php php-fpm php-redis php-yaml apache2-utils
PHPFPMINI=$(sudo find /etc/ \(  -name "php.ini" \) |grep fpm)
sudo sed -i 's/;cgi.fix_pathinfo=1/cgi.fix_pathinfo=0/g' $PHPFPMINI
WWWCONF=$(sudo find /etc/ \(  -name "www.conf" \))
sudo sed -i 's/user = www-data/user = pi/g' $WWWCONF
sudo sed -i 's/group = www-data/group = pi/g' $WWWCONF
PHPFPMSERVICE=$(sudo systemctl -a |grep fpm.service|awk '{print $1}'|grep php)
sudo systemctl restart $PHPFPMSERVICE
sudo systemctl enable $PHPFPMSERVICE

sudo rm $wwwdir/index.nginx-debian.html


for item in index.php index_html.php index.js jquery.min.js rpims.php
   do sudo mv $installdir/$item $wwwdir/
done

for item in .htpasswd rpims.yaml zabbix_rpims_userparameter.conf rpims-stream.conf
   do sudo mv $installdir/$item $wwwdir/conf/
done

for item in index.css w3.css w3-colors-2020.css
   do sudo mv $installdir/$item $wwwdir/css/
done

for item in setup.php setup_html.php setup_form.php setup.js
   do sudo mv $installdir/$item $wwwdir/setup/
done
sudo ln -s $wwwdir/setup/setup.php $wwwdir/setup/index.php

mv $installdir/ap /var/www/html

for item in hls.js hls.min.js hls.min.js.map stream.html
   do sudo mv $installdir/$item $wwwdir/stream/
done

sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.org
sudo mv $installdir/nginx-default /etc/nginx/sites-available/default
sudo chown -R pi.pi $wwwdir
sudo systemctl restart nginx
sudo systemctl enable nginx

sudo apt-get -y install zabbix-agent
echo 'zabbix ALL=(ALL) NOPASSWD: /home/pi/scripts/RPiMS/redis-get-data.py' | sudo EDITOR='tee -a' visudo

for item in zabbix_rpims_userparameter.conf zabbix_rpims.conf zabbix_agentd.conf zabbix_agentd.psk
    do sudo mv $installdir/$item $wwwdir/conf/
done

echo "Generating a unique TLSPSKIdentity"
TLSPSKIdentity=$(openssl rand -hex 8)
sed -i "s/ TLSPSKIdentity: .*/\ \TLSPSKIdentity: ${TLSPSKIdentity}/g" $wwwdir/conf/rpims.yaml
sed -i "s/TLSPSKIdentity=.*/TLSPSKIdentity=${TLSPSKIdentity}/g" $wwwdir/conf/zabbix_agentd.conf

echo "Generating a unique TLSPSK"
TLSPSK=$(openssl rand -hex 32)
sed -i "s/ TLSPSK: .*/\ \TLSPSK: ${TLSPSK}/g" $wwwdir/conf/rpims.yaml
echo $TLSPSK | sudo tee $wwwdir/conf/zabbix_agentd.psk

sudo systemctl restart zabbix-agent.service
sudo systemctl enable zabbix-agent.service

cat $installdir/motd |sudo tee /etc/update-motd.d/20-rpims
sudo chmod ugo+x  /etc/update-motd.d/20-rpims
rm $installdir/motd

cat $installdir/cron |sudo tee /etc/cron.d/rpims
sudo chown root.root /etc/cron.d/rpims
rm $installdir/cron

sudo mv $installdir/rpims.service /lib/systemd/system/rpims.service
sudo mv $installdir/rpims-stream.service /lib/systemd/system/rpims-stream.service
sudo systemctl daemon-reload
sudo systemctl enable rpims.service
#sudo systemctl enable rpims-stream.service

#for DHT22 sensor
sudo -H pip3 install --upgrade Adafruit_DHT adafruit-circuitpython-dht
sudo apt-get -y install libgpiod2 libgpiod-dev
#cd ~
#git clone https://github.com/michaellass/libgpiod_pulsein.git
#cd libgpiod_pulsein
#git checkout cpu-fix
#cd src
#make
#cd ~/.local/lib/python3.7/site-packages/adafruit_blinka/microcontroller/bcm283x/pulseio/
#cd /usr/local/lib/python3.7/dist-packages/adafruit_blinka/microcontroller/bcm283x/pulseio/
#sudo cp libgpiod_pulsein libgpiod_pulsein.bak
#sudo cp ~/libgpiod_pulsein/src/libgpiod_pulsein ./
#

_IP=$(ip route get 1.1.1.1 | awk '{print $7}')
echo ""
echo "-------------------------------------"
echo "Installation successfully completed !"
echo "-------------------------------------"
echo ""
echo "After restarting open http://$_IP/setup or http://127.0.0.1 to configure RPiMS"
echo ""
echo "Do you want to reboot RPiMS now ?"
echo ""

read -r -p "$1 [y/N] " response < /dev/tty

if [[ $response =~ ^(yes|y|Y)$ ]]; then
    sudo reboot
else
    echo ""
    echo "Run this command manually: sudo reboot"
    echo ""
    echo "After restarting open http://$_IP/setup or http://127.0.0.1/setup to configure RPiMS"
    exit
fi
