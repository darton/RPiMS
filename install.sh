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

[[ -d $INSTALLDIR ]] || mkdir -p $INSTALLDIR

cp -R $UNPACKDIR/www/* $WWWDIR
cp $UNPACKDIR/RPiMS/* $INSTALLDIR
chmod u+x $INSTALLDIR/*.py $INSTALLDIR/*.sh
chown -R pi.pi $INSTALLDIR


rm $WWWDIR/index.nginx-debian.html
mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.org
cp $UNPACKDIR/etc/nginx-default /etc/nginx/sites-available/default
cp $UNPACKDIR/etc/nginx.conf /etc/nginx
chown root.root /etc/nginx/nginx.conf
chown -R pi.www-data /var/www

echo 'zabbix ALL=(ALL) NOPASSWD: /home/pi/scripts/RPiMS/redis-get-data.py' | EDITOR='tee -a' visudo

echo "Generating a unique TLSPSKIdentity"
TLSPSKIdentity=$(openssl rand -hex 8)
sed -i "s/ TLSPSKIdentity: .*/\ \TLSPSKIdentity: ${TLSPSKIdentity}/g" $WWWDIR/conf/rpims.yaml
sed -i "s/TLSPSKIdentity=.*/TLSPSKIdentity=${TLSPSKIdentity}/g" $WWWDIR/conf/zabbix_agentd.conf

echo "Generating a unique TLSPSK"
TLSPSK=$(openssl rand -hex 32)
sed -i "s/ TLSPSK: .*/\ \TLSPSK: ${TLSPSK}/g" $WWWDIR/conf/rpims.yaml
echo $TLSPSK | tee $WWWDIR/conf/zabbix_agentd.psk

cp $UNPACKDIR/etc/zabbix_rpims.conf /etc/zabbix/zabbix_agentd.conf.d/

cat $UNPACKDIR/etc/motd |tee /etc/update-motd.d/20-rpims
chmod ugo+x /etc/update-motd.d/20-rpims

cat $UNPACKDIR/etc/cron |tee /etc/cron.d/rpims
chown root.root /etc/cron.d/rpims


cp $UNPACKDIR/etc/rpims.service /lib/systemd/system/rpims.service
cp $UNPACKDIR/etc/rpims-watcher.path /lib/systemd/system/rpims-watcher.path
cp $UNPACKDIR/etc/rpims-watcher.service /lib/systemd/system/rpims-watcher.service
cp $UNPACKDIR/etc/gunicorn.service /lib/systemd/system/gunicorn.service

systemctl daemon-reload
systemctl enable rpims.service
systemctl enable rpims-watcher.path
systemctl enable rpims-watcher.service
systemctl enable gunicorn.service

rm $DOWNLOADDIR/RPiMS.zip
rm -rf $UNPACKDIR


