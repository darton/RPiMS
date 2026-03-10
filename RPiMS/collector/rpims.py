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

from system.lock import acquire_lock
from core.run import run_collector

logging.basicConfig(
    level=logging.INFO,
    format="RPiMS-collector: %(levelname)s: %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger("RPiMS-collector")

if __name__ == "__main__":
    lock = acquire_lock()
    try:
        run_collector()
    except KeyboardInterrupt:
        logger.info("# RPiMS is stopped #")
        sys.exit(0)
    except Exception as err:
        logger.error(err)
        sys.exit(1)
