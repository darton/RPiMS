#!/usr/bin/env bash

#  Author : Dariusz Kowalczyk
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License Version 2 as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

config_file=/opt/RPiMS/config/zabbix_rpims.conf
identity=$(awk -F= '/TLSPSKIdentity/ {print $2}' $config_file)
psk="--tls-connect psk --tls-psk-identity $identity --tls-psk-file=\"/opt/RPiMS/config/zabbix_rpims.psk\""
zabbix_server=$(awk -F= '/^ServerActive=/{print $2}' $config_file)
timeout=2
key="trap"
value="$2"
location="$3"
option="$1"

zabbix_sender_cmd="zabbix_sender -vv -c "$config_file" -t "$timeout" -s "$location" -k "$key" "

case "$option" in

    'info_when_door_is_opened')
        $zabbix_sender_cmd -o "\"$value is opened\""
    ;;

    'info_when_door_is_closed')
        $zabbix_sender_cmd -o "\"$value is closed\""
    ;;

    'info_when_door_has_been_opened')
        $zabbix_sender_cmd -o "\"$value has been opened\""
    ;;

    'info_when_door_has_been_closed')
        $zabbix_sender_cmd -s "$location" -o "\"$value has been closed\""
    ;;

    'info_when_motion')
        $zabbix_sender_cmd -o "\"$value motion was detected\""
    ;;

    'info_when_no_motion')
        $zabbix_sender_cmd -o "\"$value no motion\""
    ;;

           *)
        echo -e "\nUsage: zabbix_sender.sh key sensor_id location"
        echo "key: info_when_door_is_opened |info_when_door_is_closed|info_when_door_has_been_opened|info_when_door_has_been_closed|info_when_motion|info_when_no_motion"
    ;;

esac
