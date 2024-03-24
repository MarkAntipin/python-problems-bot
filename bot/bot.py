import logging

from ptbcontrib.postgres_persistence import PostgresPersistence
<<<<<<< HEAD
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler, filters

from bot.handlers.code import web_app_data
=======
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ConversationHandler

>>>>>>> master
from bot.handlers.commands import (
    cancel_handler,
    code_handler,
    leaders_handler,
    set_difficult_handler,
    set_easy_handler,
    start_handler,
)
from bot.handlers.error import error_handler
from bot.handlers.onboarding import choose_level_handler, finish_onboarding_handler
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

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            States.onboarding: [
                CallbackQueryHandler(choose_level_handler)
            ],
            States.finish_onboarding: [
                CallbackQueryHandler(finish_onboarding_handler)
            ],
            States.daily_question: [
                CallbackQueryHandler(questions_handler),
            ]
        },
        persistent=True,
        name='bot',
        fallbacks=[CommandHandler('cancel', cancel_handler)],
    )
    bot.add_handler(conv_handler)

    # error handler
    bot.add_error_handler(error_handler)

    # additional commands
    bot.add_handler(CommandHandler('start', start_handler))
    bot.add_handler(CommandHandler('leaders', leaders_handler))
    bot.add_handler(CommandHandler('easy', set_easy_handler))
    bot.add_handler(CommandHandler('difficult', set_difficult_handler))

    return bot
