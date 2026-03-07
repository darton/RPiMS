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
from time import sleep
import adafruit_dht
import board

logger = logging.getLogger(__name__)


def get_dht_data(ctx):
    verbose = ctx.config.get('verbose')
    read_interval = ctx.dht_config.get('read_interval')
    dht_type = ctx.dht_config.get('type')
    pin = ctx.dht_config.get('pin')
    pin = getattr(board, f"D{pin}")

    debug = "no"
    delay = 0

    # selection of DHT model
    if dht_type == "DHT11":
        dht_device = adafruit_dht.DHT11(pin)
    else:
        dht_device = adafruit_dht.DHT22(pin)

    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            ctx.redis_db.hset('DHT', 'temperature', temperature)
            ctx.redis_db.hset('DHT', 'humidity', humidity)
            ctx.redis_db.expire('DHT', read_interval * 3)

            if verbose:
                logger.info("%s Temperature: %.1f°C", dht_type, temperature)
                logger.info("%s Humidity: %s%%", dht_type, humidity)

            delay = max(delay - 1, 0)

        except OverflowError as err:
            if debug == 'yes':
                logger.info('Problem with DHT sensor: %s', err)
            delay += 1

        except RuntimeError as err:
            if debug == 'yes':
                logger.info('Problem with DHT sensor: %s', err)
            delay += 1

        except Exception as err:
            dht_device.exit()
            raise err

        finally:
            if debug == 'yes':
                logger.info('DHT delay: %s', delay)

            ctx.redis_db.set('DHT_delay', delay)
            sleep(read_interval + delay)


