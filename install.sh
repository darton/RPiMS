
#!/bin/bash

installdir=/home/pi/RPiMS
[[ -d $installdir ]] || mkdir -p $installdir

for file in ADHT.py door-sensor.py redis-get.py redis-get-logdata.py stream.sh videorecorder.sh zabbix_sender.sh README.md index.php; do
curl -sS https://raw.githubusercontent.com/darton/RPiMS/master/$file > $scriptsdir/$file
done

