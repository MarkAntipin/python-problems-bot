import logging


def setup_logger() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('ptbcontrib').setLevel(logging.WARNING)
