import logging

from .config import get_logging_config


def init_logger(is_debug: bool = False, name: str = '') -> None:
    config = get_logging_config(name=name, is_debug=is_debug)
    logging.config.dictConfig(config)
