#!/bin/bash

#_IP=$(hostname -I | awk '{print $1}') || true
_IP=$(ip route get 1.1.1.1 | awk '{print $7}') || true

if [ "$_IP" ]; then
  /usr/bin/redis-cli set hostip $_IP
fi

_hostname=$(/usr/bin/redis-cli get hostname)
hostnamectl set-hostname $_hostname

_location=$(/usr/bin/redis-cli get localtion)
hostnamectl set-location "$_location"

_chassis=$(/usr/bin/redis-cli get chassis)
hostnamectl set-chassis $_chassis

_deployment=$(/usr/bin/redis-cli get deployment)
hostnamectl set-deployment $_deployment

exit 0
