#!/bin/bash

_IP=$(ip route get 1.1.1.1 | awk '{print $7}')

if [ "$_IP" ]; then
    /usr/bin/redis-cli set hostip $_IP
fi

exit 0
