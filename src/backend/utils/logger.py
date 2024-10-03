import logging

import colorlog

from backend.config import Config

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, Config.LOG_LEVEL))

console_handler = colorlog.StreamHandler()
console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))

colored_formatter = colorlog.ColoredFormatter(
    fmt='%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

console_handler.setFormatter(colored_formatter)
logger.addHandler(console_handler)
