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

import subprocess


def video_service(state):
    subprocess.Popen([
        'sudo', 'systemctl', state, 'mediamtx.service'
    ])


def zabbix_service(state):
    subprocess.Popen([
        'sudo', 'systemctl', state, 'zabbix-agent.service'
    ])


def set_hostnamectl(**kwargs):
    hctldict = {
        "location": "set-location",
        "chassis": "set-chassis",
        "deployment": "set-deployment",
    }

    # set hostname
    hostname = kwargs.get('hostname')
    if hostname:
        subprocess.Popen([
            'sudo', 'raspi-config', 'nonint', 'do_hostname', hostname
        ])

    # use hostnamectl
    for key, action in hctldict.items():
        value = kwargs.get(key)
        if value:
            subprocess.Popen([
                'sudo', '/usr/bin/hostnamectl', action, value
            ])


def get_hostinfo():
    _cmd = 'sudo ../scripts/gethostinfo.sh'
    subprocess.Popen(_cmd, shell=True)
