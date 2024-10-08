from logging import config

from .config import get_logging_config


def init_logger(is_debug: bool = False, name: str = '') -> None:
    cfg = get_logging_config(name=name, is_debug=is_debug)
    config.dictConfig(cfg)
