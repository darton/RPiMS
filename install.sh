#!/bin/bash

installdir=/home/pi/scripts/RPiMS

[[ -d $installdir ]] || mkdir -p $installdir
[[ -d /home/pi/Videos ]] || mkdir -p /home/pi/Videos

for file in $(curl -sS https://raw.githubusercontent.com/darton/RPiMS/master/files.txt); do
   curl -sS https://raw.githubusercontent.com/darton/RPiMS/master/$file > $installdir/$file
done

chmod u+x $installdir/*.py $installdir/*.sh

sudo apt-get -y install git python3-gpiozero python3-pip build-essential python3-dev python3-numpy python3-picamera
sudo apt-get -y install libfreetype6-dev libopenjp2-7 libtiff5 libjpeg-dev
sudo apt-get -y install python3-w1thermsensor
sudo apt-get -y install vlc ffmpegayer gpac fbi

sudo python3 -m pip install --upgrade pip setuptools wheel
sudo pip3 install Adafruit_DHT RPi.bme280 redis pid
sudo -H pip3 install --upgrade luma.oled
sudo -H pip3 install --upgrade luma.lcd

sudo apt-get -y install redis-server
sudo systemctl enable redis-server.service
sysctl -w vm.overcommit_memory=1
sysctl -w net.core.somaxconn=512
echo 'vm.overcommit_memory=1' | sudo tee -a /etc/sysctl.conf
echo 'net.core.somaxconn=512' | sudo tee -a /etc/sysctl.conf
echo 'maxmemory 100mb' | sudo tee -a /etc/redis/redis.conf
sudo systemctl start redis-server.service

sudo apt -y install nginx php php-fpm php-redis
sudo systemctl restart php7.3-fpm
sudo systemctl enable php7.3-fpm
sudo mv $installdir/index.php /var/www/html/
sudo rm /var/www/html/*.html
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.org
sudo mv $installdir/nginx-default /etc/nginx/sites-available/default
sudo systemctl restart nginx
sudo systemctl enable nginx

sudo apt-get -y install zabbix-agent
echo 'zabbix ALL=(ALL) NOPASSWD: /home/pi/scripts/RPiMS/redis-get-data.py' | sudo EDITOR='tee -a' visudo
cat $installdir/zabbix-rpims.conf | sed s/TLSPSKIdentity=/TLSPSKIdentity=$(openssl rand -hex 8)/ |sudo tee /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf
rm cat $installdir/zabbix-rpims.conf
openssl rand -hex 32 | sudo tee /etc/zabbix/zabbix_agentd.conf.d/zabbix_agentd.psk
sudo systemctl restart zabbix-agent.service
sudo systemctl enable zabbix-agent.service

cat $installdir/motd |sudo tee /etc/update-motd.d/20-rpims
sudo chmod ugo+x  /etc/update-motd.d/20-rpims

sudo mv $installdir/rpims.service /lib/systemd/system/rpims.service
sudo systemctl enable rpims.service
sudo systemctl start rpims.service

#cat $installdir/rc.local |sudo tee /etc/rc.local
#rm $installdir/rc.local

echo "#Uncomment sensor you want
#* * * * * pi $installdir/BME280.py > /dev/null 2>&1
#* * * * * pi $installdir/DS18B20.py > /dev/null 2>&1
* * * * * pi $installdir/CPUtemp.py > /dev/null 2>&1
" |sudo tee /etc/cron.d/rpims
