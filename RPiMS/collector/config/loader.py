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
from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

logger = logging.getLogger(__name__)


def load_config(path_to_config: str | Path) -> dict:
    """
    Loads YAML configuration file using ruamel.yaml.

    Args:
        path_to_config: Path to the configuration file

    Returns:
        dict: Loaded configuration

    Raises:
        SystemExit: When the file cannot be loaded, parsed, or is empty
    """
    yaml = YAML(typ='safe')           # safe mode – does not execute arbitrary Python code
    yaml.allow_duplicate_keys = False  # more strict parsing (optional)

    config_path = Path(path_to_config)

    try:
        with config_path.open('r', encoding='utf-8') as file:
            config = yaml.load(file)

        if config is None:
            logger.error("Configuration file is empty: %s", config_path)
            sys.exit(255)

        if not isinstance(config, dict):
            logger.error("Configuration root is not a dictionary: %s", config_path)
            sys.exit(255)

        return config

    except FileNotFoundError:
        logger.error("Configuration file not found: %s", config_path)
        sys.exit(255)

    except YAMLError as err:
        logger.error("YAML syntax error in configuration file: %s", config_path)
        logger.error(str(err))
        if hasattr(err, 'context') and err.context:
            logger.error("Context: %s", err.context)
        sys.exit(255)

    except Exception as err:
        logger.exception("Unexpected error while loading configuration: %s", config_path)
        sys.exit(255)
