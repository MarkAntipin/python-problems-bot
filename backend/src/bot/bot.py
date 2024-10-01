from ptbcontrib.postgres_persistence import PostgresPersistence
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    filters,
)

from settings import PostgresSettings, bot_settings
from src.bot.handlers.commands import (
    get_achievements_handler,
    leaders_handler,
    start_handler,
)
from src.bot.handlers.error import error_handler
from src.bot.handlers.payment import pre_checkout_handler, successful_payment_handler
from src.utils.logger import setup_logger


def create_bot() -> Application:
    setup_logger()

    pg_settings = PostgresSettings()
    persistence = PostgresPersistence(url=pg_settings.url_for_persistence)
    bot = Application.builder().token(bot_settings.TOKEN).persistence(persistence).build()

    # error handler
    bot.add_error_handler(error_handler)

    # commands
    bot.add_handler(CommandHandler('start', start_handler))
    bot.add_handler(CommandHandler('leaders', leaders_handler))
    bot.add_handler(CommandHandler('achievements', get_achievements_handler))

    bot.add_handler(PreCheckoutQueryHandler(pre_checkout_handler))
    bot.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_handler))

    return bot
