import json
import logging
import os


def setup_logger(config_file: str = 'logging_config.json') -> None:
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, config_file)
    with open(file_path, 'r') as file:
        config = json.load(file)
        logging.config.dictConfig(config)
