#!/bin/bash

repourl=https://github.com/darton/RPiMS/archive/refs/heads/master.zip
downloaddir=/tmp
unpackdir=/tmp/RPiMS-master
installdir=/home/pi/scripts/RPiMS
wwwdir=/var/www/html
_IP=$(ip route get 1.1.1.1 | awk '{print $7}')

echo "Do you want to upgrade the RPiMS ?"
read -r -p "$1 [y/N] " response < /dev/tty
#read -r -p "$1 [y/N] "
if [[ $response =~ ^(yes|y|Y)$ ]]; then
    echo "Greats ! The upgrade process has started."
    [[ -d $wwwdir ]] || sudo mkdir -p $wwwdir
    [[ -d $installdir ]] || mkdir -p $installdir
    [[ -d /home/pi/Videos ]] || mkdir -p /home/pi/Videos
    [[ ! -d $unpackdir ]] || rm -rf $unpackdir
    [[ ! -f $downloaddir/RPiMS.zip ]] || rm $downloaddir/RPiMS.zip

    curl -sS $repourl -L -o $downloaddir/RPiMS.zip
    unzip  $downloaddir/RPiMS.zip -d $downloaddir

    sudo rm -rf $installdir/*
    sudo cp $unpackdir/RPiMS/* $installdir
    sudo chmod u+x $installdir/*.py $installdir/*.sh

    for item in api css js setup
    do
	sudo rm -rf $wwwdir/$item
    done
    sudo rm $wwwdir/*.*

    for item in api css js setup
    do
	sudo cp -R $unpackdir/www/$item $wwwdir
    done

    sudo cp $unpackdir/www/*.php $wwwdir
    sudo cp $unpackdir/www/favicon.ico $wwwdir

    [[ ! -d $unpackdir ]] || rm -rf $unpackdir
    [[ ! -f $downloaddir/RPiMS.zip ]] || rm $downloaddir/RPiMS.zip

    echo ""
    echo "-------------------------------------"
    echo "Upgrade successfully completed !"
    echo "-------------------------------------"
    echo ""
fi

echo "Do you want to upgrade the Python library ?"
read -r -p "$1 [y/N] " response < /dev/tty
if [[ $response =~ ^(yes|y|Y)$ ]]; then
    echo "Greats ! The upgrade OS has started."

    sudo python3 -m pip install --upgrade pip setuptools wheel
    sudo -H pip3 install --upgrade RPi.bme280 smbus2 redis hiredis pid PyYAML luma.oled luma.lcd adafruit-circuitpython-ads1x15 rshell pyusb

    echo ""
    echo "-------------------------------------"
    echo "Upgrade successfully completed !"
    echo "-------------------------------------"
    echo ""
fi

echo "Do you want to upgrade the Operating System ?"
read -r -p "$1 [y/N] " response < /dev/tty
if [[ $response =~ ^(yes|y|Y)$ ]]; then
    echo "Greats ! The upgrade OS has started."
    sudo apt-get -y update
    sudo apt-get -y upgrade
    sudo apt-get -y autoremove

    echo ""
    echo "-------------------------------------"
    echo "Upgrade successfully completed !"
    echo "-------------------------------------"
    echo ""
fi

echo ""
echo "Do you want to reboot RPiMS now ?"
echo ""
echo "After restarting open http://$_IP/setup or http://127.0.0.1 to configure RPiMS"

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
