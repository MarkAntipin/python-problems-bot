import logging.config

from src.utils.logging.config import get_logging_config


def init_logger():
    logging.config.dictConfig(get_logging_config())
