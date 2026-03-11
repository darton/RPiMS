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
from time import sleep, time
import datetime

from luma.core.interface.serial import i2c, spi # type: ignore
from luma.core.render import canvas # type: ignore
from luma.oled.device import sh1106 # type: ignore
from luma.lcd.device import st7735 # type: ignore
from PIL import ImageFont # type: ignore
from sensors.bme280 import read_bme280

logger = logging.getLogger(__name__)

def serial_displays(ctx):
    display_type = ctx.serial_bus_display.get('display_type')
    rotate = ctx.serial_bus_display.get('display_rotate')
    refresh_rate = ctx.serial_bus_display.get('display_refresh_rate')
    serial_type = ctx.serial_bus_display.get('bus_display_type')
    font = ImageFont.load_default()
    padding = 0
    top = padding
    x = 0

    # interface selection
    if serial_type == 'i2c':
        serial = i2c(port=1, address=0x3c)
    else:
        serial = spi(
            device=0,
            port=0,
            bus_speed_hz=8000000,
            transfer_size=4096,
            gpio_DC=24 if display_type == 'oled_sh1106' else 25,
            gpio_RST=25 if display_type == 'oled_sh1106' else 27
        )

    try:
        # device selection
        if display_type == 'oled_sh1106':
            device = sh1106(serial, rotate=rotate)

        elif display_type == 'lcd_st7735':
            device = st7735(
                serial,
                width=128,
                height=128,
                h_offset=1,
                v_offset=2,
                bgr=True,
                persist=False,
                rotate=rotate
            )

        else:
            logger.error("Unknown serial display type: %s", display_type)
            return

        data_refresh_rate = 1
        last_fetch = 0
        # main display loop
        while True:
            now = time()
            if now - last_fetch >= 1/data_refresh_rate:
                sid = 'id3'

                # reading data from Redis
                bme280 = read_bme280(ctx,sid)
                t,h,p = bme280["temperature"],bme280["humidity"],bme280["pressure"]
                #logger.info('%s',bme280)

                # door and motion
                values = ctx.redis_db.hgetall('GPIO')
                doors_opened = any(v == 'open' for v in values.values())
                motion_detected = any(v == 'motion' for v in values.values())

                door_sensors = 'opened' if doors_opened else 'closed'
                motion_sensors = 'yes' if motion_detected else 'no'

                # CPU temp
                cputemp = ctx.redis_db.get('CPU_Temperature')
                cputemp = '----' if cputemp is None else round(float(cputemp), 1)

                # IP
                hostip = ctx.redis_db.get('hostip')
                hostip = hostip if hostip else '---.---.---.---'
                last_fetch = now

            # drawing
            label_x = 0
            value_x = 77

            with canvas(device) as draw:
                if display_type == 'oled_sh1106':
                    draw.text((label_x, top),     "IP:", font=font, fill=255)
                    draw.text((15, top),     hostip, font=font, fill=255)

                    draw.text((label_x, top+9),   "Temperature:", font=font, fill=255)
                    draw.text((value_x, top+9),   f"{t}°C", font=font, fill=255)

                    draw.text((label_x, top+18),  "Humidity:", font=font, fill=255)
                    draw.text((value_x, top+18),  f"{h}%", font=font, fill=255)

                    draw.text((label_x, top+27),  "Pressure:", font=font, fill=255)
                    draw.text((value_x, top+27),  f"{p}hPa", font=font, fill=255)

                    draw.text((label_x, top+36),  "Door:", font=font, fill=255)
                    draw.text((value_x, top+36),  door_sensors, font=font, fill=255)

                    draw.text((label_x, top+45),  "Motion:", font=font, fill=255)
                    draw.text((value_x, top+45),  motion_sensors, font=font, fill=255)

                    draw.text((label_x, top+54),  "CpuTemp:", font=font, fill=255)
                    draw.text((value_x, top+54),  f"{cputemp}°C", font=font, fill=255)


                elif display_type == 'lcd_st7735':
                    now = datetime.datetime.now()

                    draw.text((x+35, top), 'R P i M S', font=font, fill="cyan")

                    draw.text((x, top+15), ' Temperature', font=font, fill="lime")
                    draw.text((x+77, top+15), f'{t} *C', font=font, fill="lime")

                    draw.text((x, top+28), ' Humidity', font=font, fill="lime")
                    draw.text((x+77, top+28), f'{h} %', font=font, fill="lime")

                    draw.text((x, top+41), ' Pressure', font=font, fill="lime")
                    draw.text((x+77, top+41), f'{p} hPa', font=font, fill="lime")

                    draw.text((x, top+57), ' Door', font=font, fill="yellow")
                    draw.text((x+77, top+57), door_sensors, font=font, fill="yellow")

                    draw.text((x, top+70), ' Motion', font=font, fill="yellow")
                    draw.text((x+77, top+70), motion_sensors, font=font, fill="yellow")

                    draw.text((x, top+86), ' CPUtemp', font=font, fill="cyan")
                    draw.text((x+77, top+86), f'{cputemp} *C', font=font, fill="cyan")

                    draw.text((x, top+99), ' IP', font=font, fill="cyan")
                    draw.text((x+36, top+99), hostip, font=font, fill="cyan")

                    draw.text((x+5, top+115), now.strftime("%Y-%m-%d %H:%M:%S"), font=font, fill="floralwhite")

            sleep(1 / refresh_rate)

    except Exception as err:
        logger.error(err)
