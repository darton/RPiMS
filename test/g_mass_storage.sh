#!/bin/bash

_IP=$(hostname -I) || true
FILE=OK
TMPDIR=/run/user/1000
CMD_MOUNT="sudo modprobe g_mass_storage file=/piusb.bin stall=0 removable=1 idVendor=0x0781 idProduct=0x5572 bcdDevice=0x011a iManufacturer=\"Darton\" iProduct=\"USB Storage\" iSerialNumber=\"1234567890\"5572 bcdDevice=0x011a iManufacturer=\"San\""
CMD_UNMOUNT="sudo modprobe -r g_mass_storage"
CMD_SYNC="sudo sync"

lftp <<SCRIPT
set ftp:initial-prot ""
set ftp:ssl-force true
set ftp:ssl-protect-data true
set ssl:verify-certificate false
open ftp://ftp.example.com:21
user login password
lcd $TMPDIR
cd /private
get $FILE POWEROFF
mv $FILE DONE-$_IP
rm POWEROFF
exit
SCRIPT


if [[ -f "$TMPDIR/$FILE" ]]; then
[[ -d /mnt/usb_share ]] || mkdir /mnt/usb_share
rm -f -r /mnt/usb_share/*

lftp <<SCRIPT
set ftp:initial-prot ""
set ftp:ssl-force true
set ftp:ssl-protect-data true
set ssl:verify-certificate false
open ftp://ftp.example.com:21
user login password
lcd /mnt/usb_share
cd /private
mget *.nc
exit
SCRIPT
rm $TMPDIR/$FILE

eval $CMD_SYNC
sleep 1
eval $CMD_UNMOUNT
sleep 1
eval $CMD_SYNC
sleep 1
eval $CMD_MOUNT

fi


if [[ -f "$TMPDIR/POWEROFF" ]]; then
    rm $TMPDIR/POWEROFF
    sudo poweroff
fi
