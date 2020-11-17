#!/bin/bash

_IP=$(ip route get 1.1.1.1 | awk '{print $7}')

if [ "$_IP" ]; then
    /usr/bin/redis-cli set hostip "$_IP"
fi

_UPTIME=$(/usr/bin/uptime -s)
/usr/bin/redis-cli set uptime "$_UPTIME"

_FSUSED=$(df -h| awk '/root/ {print $5}')
/usr/bin/redis-cli set fsused "$_FSUSED"

_MEMUSED=$(free -m |awk '/Mem/ {print $3}')
/usr/bin/redis-cli set memused "$_MEMUSED"

exit 0
