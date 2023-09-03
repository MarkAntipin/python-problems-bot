import logging
from pathlib import Path

from ptbcontrib.ptb_jobstores.mongodb import PTBMongoDBJobStore
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    PicklePersistence,
)

from bot.handlers.comands import cansel_handler, start_handler
from bot.handlers.questions import onboarding_questions_handler, questions_handler
from bot.handlers.states import States
from settings import BotSettings, MongoSettings, BOT_DATA, PostgresSettings
from ptbcontrib.postgres_persistence import PostgresPersistence


def _setup_logging() -> None:
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)


def create_bot(bot_settings: BotSettings) -> Application:
    _setup_logging()

    pg_settings = PostgresSettings()
    persistence = PostgresPersistence(url=pg_settings.url_for_persistence)
    bot = Application.builder().token(bot_settings.TOKEN).persistence(persistence).build()
    mongo_settings = MongoSettings()
    bot.job_queue.scheduler.add_jobstore(
        PTBMongoDBJobStore(
            application=bot,
            host=mongo_settings.url
        )
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_handler)],
        states={
            States.onboarding_question: [
                CallbackQueryHandler(onboarding_questions_handler),
                CommandHandler("start", start_handler)
            ],
            States.daily_question: [
                CallbackQueryHandler(questions_handler),
                CommandHandler("start", start_handler)
            ]
        },
        persistent=True,
        name='bot',
        fallbacks=[CommandHandler("cancel", cansel_handler)],
    )
    bot.add_handler(conv_handler)

    return bot
