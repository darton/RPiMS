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
from w1thermsensor import W1ThermSensor, SensorNotReadyError, NoSensorFoundError

logger = logging.getLogger(__name__)

def get_ds18b20_data(ctx):
    # Read configuration values with safe defaults
    verbose = ctx.config.get('verbose', False)
    read_interval = ctx.ds18b20_config.get('read_interval', 5)

    try:
        while True:
            try:
                # Detect available DS18B20 sensors
                sensors = W1ThermSensor.get_available_sensors()

                if not sensors:
                    logger.warning("No DS18B20 sensors detected")
                    sleep(read_interval)
                    continue

                for sensor in sensors:
                    try:
                        # Read temperature from sensor
                        temperature = sensor.get_temperature()
                        ctx.redis_db.hset('DS18B20', sensor.id, temperature)

                        if verbose:
                            logger.info(
                                "Sensor %s: %.2f°C",
                                sensor.id,
                                temperature
                            )

                    except SensorNotReadyError:
                        logger.warning("Sensor %s is not ready for reading", sensor.id)
                    except Exception as e:
                        logger.error("Error reading sensor %s: %s", sensor.id, e)

                # Set expiration time for Redis data
                expire_time = 10 if read_interval < 5 else read_interval * 2
                ctx.redis_db.expire('DS18B20', expire_time)

            except NoSensorFoundError:
                logger.error("No DS18B20 sensors found on the system")

            sleep(read_interval)

    except KeyboardInterrupt:
        logger.info("DS18B20 reading stopped by user (Ctrl+C)")
    except Exception as err:
        logger.exception("Unexpected DS18B20 handler error: %s", err)
