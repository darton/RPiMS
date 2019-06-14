#!/bin/bash

installdir=/home/pi/scripts/RPiMS

[[ -d $installdir ]] || mkdir -p $installdir
[[ -d /home/pi/Videos ]] || mkdir -p /home/pi/Videos

for file in ADHT.py sensors.py redis-get.py redis-get-logdata.py stream.sh videorecorder.sh zabbix_sender.sh zabbix-rpims.conf README.md index.php motd rc.local; do

   curl -sS https://raw.githubusercontent.com/darton/RPiMS/master/$file > $installdir/$file

done

chmod u+x $installdir/*.py $installdir/*.sh

sudo apt-get -y install git-core python3-gpiozero python3-pip build-essential python-dev python3-numpy redis-server php php-fpm php-redis zabbix-agent

sudo python3 -m pip install --upgrade pip setuptools wheel

sudo pip3 install Adafruit_DHT redis

sudo systemctl enable redis-server.service

sudo systemctl start redis-server.service

echo "cgi.fix_pathinfo=0" |sudo tee -a /etc/php/7.0/fpm/php.ini

sudo rm /var/www/html/index.html

sudo a2enmod proxy_fcgi setenvif

sudo a2enconf php7.0-fpm

sudo systemctl restart php7.0-fpm

sudo systemctl enable php7.0-fpm

sudo systemctl restart apache2

sudo mv $installdir/index.php /var/www/html/

#curl -sS https://raw.githubusercontent.com/darton/RPiMS/master/nginx/default > $installdir/nginx.default

#sudo systemctl enable nginx

#sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.org

#sudo mv $installdir/nginx.default /etc/nginx/sites-available/

#sudo systemctl restart nginx

echo 'zabbix ALL=(ALL) NOPASSWD: /home/pi/scripts/RPiMS/redis-get.py' | sudo EDITOR='tee -a' visudo

sudo cat $installdir/zabbix-rpims.conf |sudo tee /etc/zabbix/zabbix_agentd.conf.d/zabbix-rpims.conf

sudo systemctl restart zabbix-agent.service

sudo cat $installdir/motd |sudo tee /etc/update-motd.d/20-rpims

sudo chmod ugo+x  /etc/update-motd.d/20-rpims

sudo cat $installdir/rc.local |sudo tee /etc/rc.local

echo "# Add the sensors.py as cron jobs

* * * * * pi $installdir/ADHT.py  > /dev/null 2>&1
" |sudo tee /etc/cron.d/rpims

sudo su - pi -c '/home/pi/scripts/RPiMS/sensors.py &'


