#!/bin/bash

repourl=https://github.com/darton/RPiMS/archive/refs/heads/master.zip
downloaddir=/tmp
unpackdir=/tmp/RPiMS-master
installdir=/home/pi/scripts/RPiMS
wwwdir=/var/www/html

INSTALL_CMD="sudo apt-get -y install"
PIP3_INSTALL_CMD="sudo -H pip3 install --upgrade"

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

$INSTALL_CMD uv4l uv4l-raspicam
$INSTALL_CMD uv4l-raspicam-extras
$INSTALL_CMD uv4l-server
#$INSTALL_CMD uv4l-server uv4l-uvc uv4l-xscreen uv4l-mjpegstream uv4l-dummy uv4l-raspidisp
#$INSTALL_CMD uv4l-webrtc
#$INSTALL_CMD uv4l-webrtc-armv6
sudo mv /etc/uv4l/uv4l-raspicam.conf /etc/uv4l/uv4l-raspicam.conf.org
sudo ln -s /var/www/html/conf/uv4l-raspicam.conf /etc/uv4l/uv4l-raspicam.conf
sudo systemctl restart uv4l_raspicam

$INSTALL_CMD git
$INSTALL_CMD libfreetype6-dev
$INSTALL_CMD libopenjp2-7
$INSTALL_CMD libtiff5
$INSTALL_CMD libjpeg-dev
$INSTALL_CMD vlc
$INSTALL_CMD ffmpeg
$INSTALL_CMD gpac
$INSTALL_CMD fbi

$INSTALL_CMD build-essential
$INSTALL_CMD python3-gpiozero
$INSTALL_CMD python3-dev
$INSTALL_CMD python3-numpy
$INSTALL_CMD python3-picamera
$INSTALL_CMD python3-automationhat
$INSTALL_CMD python3-systemd
$INSTALL_CMD python3-pip
$INSTALL_CMD python3-setuptools
$INSTALL_CMD python3-wheel



$PIP3_INSTALL_CMD RPi.bme280 smbus2
$PIP3_INSTALL_CMD w1thermsensor
$PIP3_INSTALL_CMD redis hiredis
$PIP3_INSTALL_CMD pid
$PIP3_INSTALL_CMD PyYAML
$PIP3_INSTALL_CMD luma.oled luma.lcd
$PIP3_INSTALL_CMD adafruit-circuitpython-ads1x15
$PIP3_INSTALL_CMD rshell
$PIP3_INSTALL_CMD pyusb

$INSTALL_CMD redis-server
sudo systemctl enable redis-server.service
sudo sysctl -w vm.overcommit_memory=1
sudo sysctl -w net.core.somaxconn=512
echo 'vm.overcommit_memory=1' | sudo tee -a /etc/sysctl.conf
echo 'net.core.somaxconn=512' | sudo tee -a /etc/sysctl.conf
echo 'maxmemory 100mb' | sudo tee -a /etc/redis/redis.conf
sudo systemctl start redis-server.service

$INSTALL_CMD apache2-utils
$INSTALL_CMD nginx
$INSTALL_CMD php php-fpm php-redis php-yaml
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

$INSTALL_CMD zabbix-agent
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
sudo chmod ugo+x /etc/update-motd.d/20-rpims

cat $unpackdir/etc/cron |sudo tee /etc/cron.d/rpims
sudo chown root.root /etc/cron.d/rpims

sudo mv $unpackdir/etc/rpims.service /lib/systemd/system/rpims.service
sudo systemctl daemon-reload
sudo systemctl enable rpims.service


#for DHT22 sensor
$PIP3_INSTALL_CMD Adafruit_DHT adafruit-circuitpython-dht
$INSTALL_CMD libgpiod2 libgpiod-dev
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
