#!/bin/bash

zabbix_server=192.168.1.125
host_ip=`ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'`

case "$1" in

    'info_when_door_is_opened')
        zabbix_sender -z $zabbix_server -p 10051 -s "$host_ip" -k trap -o "The door is opened"
    ;;
    'info_when_door_is_closed')
        zabbix_sender -z $zabbix_server -p 10051 -s "$host_ip" -k trap -o "The door is closed"
    ;;
    'info_when_door_has_been_opened')
        zabbix_sender -z $zabbix_server -p 10051 -s "$host_ip" -k trap -o "The door has been opened"
    ;;
    'info_when_door_has_been_closed')
        zabbix_sender -z $zabbix_server -p 10051 -s "$host_ip" -k trap -o "The door has been closed"
    ;;
           *)
        echo -e "\nUsage: zabbix_sender.sh info_when_door_is_opened|info_when_door_is_closed|info_when_door_has_been_opened|info_when_door_has_been_closed"
    ;;

esac
