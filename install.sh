#!/bin/bash

installdir=/home/pi/scripts/RPiMS

[[ -d $installdir ]] || mkdir -p $installdir
[[ -d /home/pi/Videos ]] || mkdir -p /home/pi/Videos

for file in ADHT.py BME280.py CPUtemp.py DS18B20.py sensors.py redis-get.py redis-get-logdata.py stream.sh videorecorder.sh zabbix_sender.sh zabbix-rpims.conf README.md index.php nginx-default motd rc.local luma_oled.py luma_lcd.py; do
   curl -sS https://raw.githubusercontent.com/darton/RPiMS/master/$file > $installdir/$file
   sleep 1
done

chmod u+x $installdir/*.py $installdir/*.sh

sudo apt-get update
sudo apt-get dist-upgrade

sudo apt-get -y install git-core python3-gpiozero python3-pip build-essential python3-dev python3-numpy python3-picamera
sudo apt-get -y install libfreetype6-dev libopenjp2-7 libtiff5 libjpeg-dev
sudo apt-get install python3-w1thermsensor

sudo python3 -m pip install --upgrade pip setuptools wheel
sudo pip3 install Adafruit_DHT RPi.bme280 redis
sudo -H pip3 install --upgrade luma.oled
sudo -H pip3 install --upgrade luma.lcd

sudo apt-get -y install redis-server
sudo systemctl enable redis-server.service
sudo systemctl start redis-server.service

sudo apt install nginx php php-fpm php-redis
echo "cgi.fix_pathinfo=0" |sudo tee -a /etc/php/7.0/fpm/php.ini
sudo rm /var/www/html/index.html
#sudo a2enmod proxy_fcgi setenvif
#sudo a2enconf php7.0-fpm
sudo systemctl restart php7.0-fpm
sudo systemctl enable php7.0-fpm
sudo mv $installdir/index.php /var/www/html/
curl -sS https://raw.githubusercontent.com/darton/RPiMS/master/nginx.default > $installdir/nginx.default
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.org
sudo mv $installdir/nginx.default /etc/nginx/sites-available/default
sudo systemctl restart nginx
sudo systemctl enable nginx

sudo apt-get -y install zabbix-agent
echo 'zabbix ALL=(ALL) NOPASSWD: /home/pi/scripts/RPiMS/redis-get.py' | sudo EDITOR='tee -a' visudo
cat $installdir/zabbix-rpims.conf |sudo tee /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf
sudo systemctl restart zabbix-agent.service
sudo systemctl enable zabbix-agent.service

cat $installdir/motd |sudo tee /etc/update-motd.d/20-rpims
sudo chmod ugo+x  /etc/update-motd.d/20-rpims

cat $installdir/rc.local |sudo tee /etc/rc.local

echo "# Add the ADHT.py as cron jobs
#* * * * * pi $installdir/ADHT.py > /dev/null 2>&1
#* * * * * pi $installdir/BME280.py > /dev/null 2>&1
#* * * * * pi $installdir/DS18B20.py > /dev/null 2>&1
#* * * * * pi $installdir/CPUtemp.py > /dev/null 2>&1
" |sudo tee /etc/cron.d/rpims
