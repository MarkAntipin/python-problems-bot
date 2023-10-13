import logging


def get_logging_config() -> dict:
    logging_config = {
        'version': 1,
        'formatters': {
            'json_formatter': {
                '()': 'src.utils.logging.formatter.JsonFormatter'
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
                'level': 'INFO',
            }
        }
    }

    return logging_config