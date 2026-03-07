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


def read_bme280(ctx, sid, default=None):
    raw = ctx.redis_db.hgetall(f"{sid}_BME280")
    #logger.info('%s', raw)

    if not raw:
        return {
            "temperature": default,
            "humidity": default,
            "pressure": default
        }

    def to_float(v):
        try:
            return float(v)
        except (ValueError, TypeError):
            return default

    temp = to_float(raw.get("temperature"))
    hum  = to_float(raw.get("humidity"))
    pres = to_float(raw.get("pressure"))

    return {
        "temperature": round(temp, 1) if temp is not None else default,
        "humidity":    round(hum)     if hum  is not None else default,
        "pressure":    round(pres)    if pres is not None else default,
    }
