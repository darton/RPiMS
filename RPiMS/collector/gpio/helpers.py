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
from system.actions import zabbix_sender_call, mediamtx_keepalive

logger = logging.getLogger(__name__)

def door_action_closed(ctx, door_id):
    ctx.redis_db.hset('GPIO', str(door_id), 'close')
    ctx.redis_db.hset('DOOR_SENSORS', str(door_id), 'close')

    if ctx.config.get('verbose'):
        logger.info('The %s has been closed!', door_id)

    if ctx.config.get('use_zabbix_sender'):
        zabbix_sender_call(ctx, 'info_when_door_has_been_closed', door_id)


def door_action_opened(ctx, door_id):
    ctx.redis_db.hset('GPIO', str(door_id), 'open')
    ctx.redis_db.hset('DOOR_SENSORS', str(door_id), 'open')

    if ctx.config.get('verbose'):
        logger.info('The %s has been opened!', door_id)

    if ctx.config.get('use_zabbix_sender'):
        zabbix_sender_call(ctx, 'info_when_door_has_been_opened', door_id)


def door_status_open(ctx, door_id):
    ctx.redis_db.hset('GPIO', str(door_id), 'open')
    ctx.redis_db.hset('DOOR_SENSORS', str(door_id), 'open')

    if ctx.config.get('verbose'):
        logger.info('The %s is opened!', door_id)

    if ctx.config.get('use_zabbix_sender'):
        zabbix_sender_call(ctx, 'info_when_door_is_opened', door_id)


def door_status_close(ctx, door_id):
    ctx.redis_db.hset('GPIO', str(door_id), 'close')
    ctx.redis_db.hset('DOOR_SENSORS', str(door_id), 'close')

    if ctx.config.get('verbose'):
        logger.info('The %s is closed!', door_id)

    if ctx.config.get('use_zabbix_sender'):
        zabbix_sender_call(ctx, 'info_when_door_is_closed', door_id)


def motion_sensor_when_motion(ctx, ms_id):
    ctx.redis_db.hset('GPIO', str(ms_id), 'motion')
    ctx.redis_db.hset('MOTION_SENSORS', str(ms_id), 'motion')

    if ctx.config.get('verbose'):
        logger.info('The %s: motion was detected!', ms_id)

    if ctx.config.get('use_zabbix_sender'):
        zabbix_sender_call(ctx, 'info_when_motion', ms_id)


def motion_sensor_when_no_motion(ctx, ms_id):
    ctx.redis_db.hset('GPIO', str(ms_id), 'nomotion')
    ctx.redis_db.hset('MOTION_SENSORS', str(ms_id), 'nomotion')

    if ctx.config.get('verbose'):
        logger.info('The %s: no motion', ms_id)


def detect_no_alarms(ctx):
    use_door = ctx.config.get('use_door_sensor')
    use_motion = ctx.config.get('use_motion_sensor')

    # both type door and motion sensors are active
    if use_door and use_motion:
        door_values = [sensor.value for sensor in ctx.door_sensors.values()]
        motion_values = [int(not sensor.value) for sensor in ctx.motion_sensors.values()]
        return all(door_values) and all(motion_values)

    # only door sensors
    if use_door and not use_motion:
        door_values = [sensor.value for sensor in ctx.door_sensors.values()]
        return all(door_values)

    # only motion sensors
    if not use_door and use_motion:
        motion_values = [int(not sensor.value) for sensor in ctx.motion_sensors.values()]
        return all(motion_values)

    # no sensors = no alarms
    return True
