import logging

from telegram.ext import ContextTypes

from settings import IS_DEBUG
from src.utils.logging.init_logger import init_logger

init_logger(is_debug=IS_DEBUG)
logger = logging.getLogger(__name__)


async def error_handler(_: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)
