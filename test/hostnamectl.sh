#!/bin/bash

_hostname=$(/usr/bin/redis-cli get hostname)
hostnamectl set-hostname $_hostname

_location=$(/usr/bin/redis-cli get localtion)
hostnamectl set-location "$_location"

_chassis=$(/usr/bin/redis-cli get chassis)
hostnamectl set-chassis $_chassis

_deployment=$(/usr/bin/redis-cli get deployment)
hostnamectl set-deployment $_deployment

exit 0
