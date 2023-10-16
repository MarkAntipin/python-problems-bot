from typing import Dict


def get_logging_config(
        name: str = '',
        is_debug: bool = False
) -> Dict[str, any]:
    level = 'DEBUG' if is_debug else 'INFO'
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json_formatter': {
                '()': 'src.utils.logging.formatter.JSONFormatter'
            }
        },
        'handlers': {
            'stdout_handler': {
                'class': 'logging.StreamHandler',
                'formatter': 'json_formatter',
                'stream': 'ext://sys.stdout'
            }
        },
        'loggers': {
            '': {
                'handlers': ['stdout_handler'],
                'level': level,
            }
        }
    }

    return logging_config
