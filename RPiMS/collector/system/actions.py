#!/usr/bin/env python3

# -*- coding:utf-8 -*-
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

import logging
import subprocess
import socket


logger = logging.getLogger(__name__)


def shutdown():
    subprocess.check_call(['sudo', 'poweroff'])


def get_hostip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"


def old_zabbix_sender_call(message, sensor_id):
    _cmd = f'/opt/RPiMS/scripts/zabbix_sender.sh {message} {str(sensor_id)}'
    subprocess.Popen([_cmd],shell=True)


def zabbix_sender_call(ctx, key, value):
    if not ctx.config.get('use_zabbix_sender'):
        return

    try:
        subprocess.check_call([
            'zabbix_sender',
            '-c', '/opt/RPiMS/config/zabbix_rpims.conf',
            '-s', ctx.zabbix_agent.get('hostname'),
            '-k', key,
            '-o', str(value),
            ],)
    except Exception as e:
        logger.error(f"Zabbix sender error: {e}")



def mediamtx_keepalive():
    try:
        subprocess.check_call(["sudo", "systemctl", "restart", "mediamtx-keepalive.service"])
    except Exception as e:
        logger.error(f"Failed to trigger MediaMTX keepalive: {e}")
