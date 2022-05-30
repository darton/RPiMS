#!/usr/bin/env bash


if [[ $(id -u) -ne 0 ]]; then
  echo "This script must be executed as root or using sudo"
  exit 99
fi

systemd="$(ps --no-headers -o comm 1)"
if [ ! "${systemd}" = "systemd" ]; then
  echo "This system is not running systemd.  Exiting..."
  exit 100
fi

if dpkg -l | grep -Eqw "gdm3|sddm|lxdm|xdm|lightdm|slim|wdm"; then
  echo "Please use a Lite version of the image"
  echo "Exiting..."
  exit 101
fi

repourl=https://github.com/darton/RPiMS/archive/refs/heads/master.zip
downloaddir=/tmp
unpackdir=/tmp/RPiMS-master
installdir=/home/pi/scripts/RPiMS
wwwdir=/var/www/html

INSTALL_CMD="apt-get -y install"
PIP3_INSTALL_CMD="pip3 install --upgrade"

echo "Do you want to install the RPiMS software?"
read -r -p "$1 [y/N] " response < /dev/tty
if [[ $response =~ ^(yes|y|Y)$ ]]; then
    echo "Greats ! The installation has started."
else
    echo "OK. Exiting"
    exit
fi

raspi-config nonint do_i2c 0
raspi-config nonint do_spi 0
raspi-config nonint do_onewire 0
raspi-config nonint do_camera 0
#raspi-config nonint do_serial 1
raspi-config nonint do_change_timezone Europe/Warsaw

[[ -d $wwwdir ]] || mkdir -p $wwwdir
[[ -d $installdir ]] || mkdir -p $installdir
[[ -d /home/pi/Videos ]] || mkdir -p /home/pi/Videos

curl -sS $repourl -L -o $downloaddir/RPiMS.zip
unzip  $downloaddir/RPiMS.zip -d $downloaddir
cp -R $unpackdir/www/* $wwwdir
cp $unpackdir/RPiMS/* $installdir
chmod u+x $installdir/*.py $installdir/*.sh
chown -R pi.pi $installdir
systemctl stop dphys-swapfile.service
systemctl disable dphys-swapfile.service

curl https://www.linux-projects.org/listing/uv4l_repo/lpkey.asc | apt-key add -
echo "deb https://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main" | tee /etc/apt/sources.list.d/uv4l.list

apt-get -y update
apt-get -y upgrade
apt-get -y autoremove

$INSTALL_CMD uv4l uv4l-raspicam
$INSTALL_CMD uv4l-raspicam-extras
$INSTALL_CMD uv4l-server
#$INSTALL_CMD uv4l-server uv4l-uvc uv4l-xscreen uv4l-mjpegstream uv4l-dummy uv4l-raspidisp
#$INSTALL_CMD uv4l-webrtc
#$INSTALL_CMD uv4l-webrtc-armv6
mv /etc/uv4l/uv4l-raspicam.conf /etc/uv4l/uv4l-raspicam.conf.org
ln -s /var/www/html/conf/uv4l-raspicam.conf /etc/uv4l/uv4l-raspicam.conf
systemctl restart uv4l_raspicam

$INSTALL_CMD git
$INSTALL_CMD liblockfile-bin
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
systemctl enable redis-server.service
sysctl -w vm.overcommit_memory=1
sysctl -w net.core.somaxconn=512
echo 'vm.overcommit_memory=1' | tee -a /etc/sysctl.conf
echo 'net.core.somaxconn=512' | tee -a /etc/sysctl.conf
echo 'maxmemory 100mb' | tee -a /etc/redis/redis.conf
systemctl start redis-server.service

$INSTALL_CMD apache2-utils
$INSTALL_CMD nginx
rm $wwwdir/index.nginx-debian.html

mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.org
mv $unpackdir/etc/nginx-default /etc/nginx/sites-available/default
mv $unpackdir/etc/nginx.conf /etc/nginx
chown root.root /etc/nginx/nginx.conf

$INSTALL_CMD gunicorn
$PIP3_INSTALL_CMD flask gunicorn

chown -R pi.www-data $wwwdir
systemctl restart nginx
systemctl enable nginx



$INSTALL_CMD zabbix-agent
echo 'zabbix ALL=(ALL) NOPASSWD: /home/pi/scripts/RPiMS/redis-get-data.py' | EDITOR='tee -a' visudo

echo "Generating a unique TLSPSKIdentity"
TLSPSKIdentity=$(openssl rand -hex 8)
sed -i "s/ TLSPSKIdentity: .*/\ \TLSPSKIdentity: ${TLSPSKIdentity}/g" $wwwdir/conf/rpims.yaml
sed -i "s/TLSPSKIdentity=.*/TLSPSKIdentity=${TLSPSKIdentity}/g" $wwwdir/conf/zabbix_agentd.conf

echo "Generating a unique TLSPSK"
TLSPSK=$(openssl rand -hex 32)
sed -i "s/ TLSPSK: .*/\ \TLSPSK: ${TLSPSK}/g" $wwwdir/conf/rpims.yaml
echo $TLSPSK | tee $wwwdir/conf/zabbix_agentd.psk

cp $unpackdir/etc/zabbix_rpims.conf /etc/zabbix/zabbix_agentd.conf.d/

systemctl restart zabbix-agent.service
systemctl enable zabbix-agent.service

cat $unpackdir/etc/motd |tee /etc/update-motd.d/20-rpims
chmod ugo+x /etc/update-motd.d/20-rpims

cat $unpackdir/etc/cron |tee /etc/cron.d/rpims
chown root.root /etc/cron.d/rpims

mv $unpackdir/etc/rpims.service /lib/systemd/system/rpims.service
systemctl daemon-reload
systemctl enable rpims.service


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
#cp libgpiod_pulsein libgpiod_pulsein.bak
#cp ~/libgpiod_pulsein/src/libgpiod_pulsein ./
#

rm $downloaddir/RPiMS.zip
#rmdir $unpackdir

hostnamectl set-hostname rpims.example.com
echo  "127.0.1.2       rpims.example.com" | tee -a /etc/hosts

_IP=$(ip route get 1.1.1.1 | awk '{print $7}')
echo ""
echo "-------------------------------------"
echo "Installation successfully completed !"
echo "-------------------------------------"
echo ""
echo "After restarting open http://$_IP/setup or http://127.0.0.1 to configure RPiMS"
echo ""
echo "Reboot is necessary for proper RPiMS operation."
echo "Do you want to reboot RPiMS now ?"
echo ""

read -r -p "$1 [y/N] " response < /dev/tty

if [[ $response =~ ^(yes|y|Y)$ ]]; then
    reboot
else
    echo ""
    echo "Run this command manually: reboot"
    echo ""
    echo "After restarting open http://$_IP/setup or http://127.0.0.1/setup to configure RPiMS"
    exit
fi
