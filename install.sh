#!/bin/bash

repourl=https://github.com/darton/RPiMS/archive/refs/heads/master.zip
downloaddir=/tmp
unpackdir=/tmp/RPiMS-master
installdir=/home/pi/scripts/RPiMS
wwwdir=/var/www/html

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

[[ -d $wwwdir ]] || sudo mkdir -p $wwwdir
[[ -d $installdir ]] || mkdir -p $installdir
[[ -d /home/pi/Videos ]] || mkdir -p /home/pi/Videos

curl -sS $repourl -L -o $downloaddir/RPiMS.zip
unzip  $downloaddir/RPiMS.zip -d $downloaddir
sudo cp -R $unpackdir/www/* $wwwdir
sudo cp $unpackdir/RPiMS/* $installdir
sudo chmod u+x $installdir/*.py $installdir/*.sh

sudo systemctl stop dphys-swapfile.service
sudo systemctl disable dphys-swapfile.service

curl https://www.linux-projects.org/listing/uv4l_repo/lpkey.asc | sudo apt-key add -
echo "deb https://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main" | sudo tee /etc/apt/sources.list.d/uv4l.list

sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y autoremove

sudo apt-get -y install uv4l uv4l-raspicam
sudo apt-get -y install uv4l-raspicam-extras
sudo apt-get -y install uv4l-server

#sudo apt-get install uv4l-server uv4l-uvc uv4l-xscreen uv4l-mjpegstream uv4l-dummy uv4l-raspidisp
#sudo apt-get install uv4l-webrtc
#sudo apt-get install uv4l-webrtc-armv6
sudo mv /etc/uv4l/uv4l-raspicam.conf /etc/uv4l/uv4l-raspicam.conf.org
sudo ln -s /var/www/html/conf/uv4l-raspicam.conf /etc/uv4l/uv4l-raspicam.conf

sudo systemctl restart uv4l_raspicam
 

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

sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.org
sudo mv $unpackdir/etc/nginx-default /etc/nginx/sites-available/default
sudo mv $unpackdir/etc/nginx.conf /etc/nginx
sudo chown root.root /etc/nginx/nginx.conf
sudo chown -R pi.pi $wwwdir
sudo systemctl restart nginx
sudo systemctl enable nginx

sudo apt-get -y install zabbix-agent
echo 'zabbix ALL=(ALL) NOPASSWD: /home/pi/scripts/RPiMS/redis-get-data.py' | sudo EDITOR='tee -a' visudo

echo "Generating a unique TLSPSKIdentity"
TLSPSKIdentity=$(openssl rand -hex 8)
sed -i "s/ TLSPSKIdentity: .*/\ \TLSPSKIdentity: ${TLSPSKIdentity}/g" $wwwdir/conf/rpims.yaml
sed -i "s/TLSPSKIdentity=.*/TLSPSKIdentity=${TLSPSKIdentity}/g" $wwwdir/conf/zabbix_agentd.conf

echo "Generating a unique TLSPSK"
TLSPSK=$(openssl rand -hex 32)
sed -i "s/ TLSPSK: .*/\ \TLSPSK: ${TLSPSK}/g" $wwwdir/conf/rpims.yaml
echo $TLSPSK | sudo tee $wwwdir/conf/zabbix_agentd.psk

sudo cp $unpackdir/etc/zabbix_rpims.conf /etc/zabbix/zabbix_agentd.conf.d/

sudo systemctl restart zabbix-agent.service
sudo systemctl enable zabbix-agent.service

cat $unpackdir/etc/motd |sudo tee /etc/update-motd.d/20-rpims
sudo chmod ugo+x  /etc/update-motd.d/20-rpims

cat $unpackdir/etc/cron |sudo tee /etc/cron.d/rpims
sudo chown root.root /etc/cron.d/rpims

sudo mv $unpackdir/etc/rpims.service /lib/systemd/system/rpims.service
sudo systemctl daemon-reload
sudo systemctl enable rpims.service



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

rm $downloaddir/RPiMS.zip
#rmdir $unpackdir

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
