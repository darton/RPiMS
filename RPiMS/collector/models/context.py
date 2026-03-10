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

class AppContext:
    def __init__(self, gpio, config, zabbix_agent, sensors, redis_db):
        self.gpio = gpio
        self.config = config
        self.zabbix_agent = zabbix_agent
        self.sensors = sensors
        self.redis_db = redis_db

        # sensors subset:
        self.bme280_config = sensors['BME280']
        self.dht_config = sensors['DHT']
        self.cputemp_config = sensors['CPU']['temp']
        self.ds18b20_config = sensors['ONE_WIRE']['DS18B20']
        self.rainfall_config = sensors['WEATHER']['RAINFALL']
        self.windspeed_config = sensors['WEATHER']['WIND']['SPEED']
        self.winddirection_config = sensors['WEATHER']['WIND']['DIRECTION']

        # gpio supsets
        self.door_sensors = {}
        self.motion_sensors = {}
        self.system_buttons = {}
        self.led_indicators = {}


class SensorContext:
    def __init__(self, app_context, sensor_name, sensor_config):
        self.app = app_context          # global AppContext
        self.name = sensor_name         # for example "id3"
        self.config = sensor_config     # config specific sensor



