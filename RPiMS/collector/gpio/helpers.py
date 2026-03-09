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

    if ctx.config.get('use_picamera') and ctx.config.get('use_picamera_recording'):
        mediamtx_keepalive(ctx)


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

    if ctx.config.get('use_picamera') and ctx.config.get('use_picamera_recording'):
        mediamtx_keepalive(ctx)


def motion_sensor_when_no_motion(ctx, ms_id):
    ctx.redis_db.hset('GPIO', str(ms_id), 'nomotion')
    ctx.redis_db.hset('MOTION_SENSORS', str(ms_id), 'nomotion')

    if ctx.config.get('verbose'):
        logger.info('The %s: no motion', ms_id)
