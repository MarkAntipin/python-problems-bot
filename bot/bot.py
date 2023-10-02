import logging

from ptbcontrib.postgres_persistence import PostgresPersistence
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ConversationHandler

from bot.handlers.comands import cansel_handler, leaders_handler, start_handler
from bot.handlers.error import error_handler
from bot.handlers.questions import questions_handler
from bot.handlers.states import States
from settings import BotSettings, PostgresSettings


def _setup_logging() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('ptbcontrib').setLevel(logging.WARNING)


def create_bot() -> Application:
    _setup_logging()

    bot_settings = BotSettings()
    pg_settings = PostgresSettings()
    persistence = PostgresPersistence(url=pg_settings.url_for_persistence)
    bot = Application.builder().token(bot_settings.TOKEN).persistence(persistence).build()

    leaders_handler_command = CommandHandler('leaders', leaders_handler)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            States.daily_question: [
                CallbackQueryHandler(questions_handler),
                CommandHandler('start', start_handler),
            ]
        },
        persistent=True,
        name='bot',
        fallbacks=[CommandHandler('cancel', cansel_handler)],
    )
    bot.add_handler(conv_handler)
    bot.add_handler(leaders_handler_command)
    bot.add_error_handler(error_handler)

    return bot
