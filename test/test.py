import logging
import logging.config
import time

import yaml
from loguru import logger

new_level = logger.level("SNAKY", no=38, color="<yellow>", icon="🐍")

logger.log("SNAKY", "Here we go!")