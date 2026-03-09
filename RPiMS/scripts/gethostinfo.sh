#!/usr/bin/env bash

#
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

redis_cmd='timeout 2 /usr/bin/redis-cli'

if [[ $(id -u) -ne 0 ]]; then
  echo "This script must be executed as root or using sudo"
  exit 1
fi

_IP=$(ip route get 1.1.1.1 | awk '/1.1.1.1/{print $7}')

if [ "$_IP" ]; then
    $redis_cmd set hostip "$_IP" 2>&1 > /dev/null
fi

_UPTIME=$(/usr/bin/uptime -s)
$redis_cmd set uptime "$_UPTIME" 2>&1 > /dev/null

_FSUSED=$(df -h| awk '/root/ {print $5}')
$redis_cmd set fsused "$_FSUSED" 2>&1 > /dev/null

_MEMUSED=$(free -m |awk '/Mem/ {print $3}')
$redis_cmd set memused "$_MEMUSED" 2>&1 > /dev/null

exit 0
