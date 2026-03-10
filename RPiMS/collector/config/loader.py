import logging
import sys
import yaml

logger = logging.getLogger(__name__)

def config_load(path_to_config):
    try:
        with open(path_to_config, mode='r') as file:
            config_yaml = yaml.full_load(file)
        return config_yaml
    except Exception as err:
        logger.error(err)
        logger.error = ("Can't load RPiMS config file: %s", path_to_config)
        sys.exit(255)
