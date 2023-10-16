import logging.config

from src.utils.logging.config import get_logging_config


def init_logger(
        is_debug: bool = False,
        name: str = '',
) -> None:
    logging.config.dictConfig(get_logging_config(name=name, is_debug=is_debug))
