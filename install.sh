#!/bin/bash

installdir=/home/pi/RPiMS

[[ -d $installdir ]] || mkdir -p $installdir

for file in ADHT.py door-sensor.py redis-get.py redis-get-logdata.py stream.sh videorecorder.sh zabbix_sender.sh README.md index.php; do

  curl -sS https://raw.githubusercontent.com/darton/RPiMS/master/$file > $installdir/$file

done

chmod u+x *.py *.sh

sudo apt-get -y install git-core python3-gpiozero python3-pip build-essential python-dev python3-numpy redis-server nginx php php-fpm php-redis zabbix-agent

sudo python3 -m pip install --upgrade pip setuptools wheel

sudo pip3 install Adafruit_DHT redis

sudo systemctl enable redis-server.service

sudo systemctl start redis-server.service

sudo systemctl enable php7.0-fpm

sudo systemctl enable nginx

echo "cgi.fix_pathinfo=0" |sudo tee -a /etc/php/7.0/fpm/php.ini

sudo systemctl restart php7.0-fpm

mv $installdir/index.php /var/www/html/

exit
