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
import sys
import redis

logger = logging.getLogger(__name__)

def db_connect(dbhost, dbnum):
    try:
        redis_db = redis.StrictRedis(host=dbhost, port=6379, db=str(dbnum), decode_responses=True)
        redis_db.ping()
        return redis_db
    except Exception as err:
        logger.error(err)
        logger.error("Can't connect to RedisDB host: %s", dbhost)
        sys.exit(255)
