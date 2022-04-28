#!/usr/bin/env bash

_IP=$(ip route get 1.1.1.1 | awk '{print $7}')

if [ "$_IP" ]; then
    /usr/bin/redis-cli hset SYSTEM hostip "$_IP" 2>&1 > /dev/null
fi

_UPTIME=$(/usr/bin/uptime -s)
/usr/bin/redis-cli hset SYSTEM uptime "$_UPTIME" 2>&1 > /dev/null

_FSUSED=$(df -h| awk '/root/ {print $5}')
/usr/bin/redis-cli hset SYSTEM fsused "$_FSUSED" 2>&1 > /dev/null

_MEMUSED=$(free -m |awk '/Mem/ {print $3}')
/usr/bin/redis-cli hset SYSTEM memused "$_MEMUSED MB" 2>&1 > /dev/null

exit 0
