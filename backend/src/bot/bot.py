from ptbcontrib.postgres_persistence import PostgresPersistence
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
    filters,
)

from settings import PostgresSettings, bot_settings
from src.bot.handlers.change_level import change_level_handler, choose_level_command
from src.bot.handlers.commands import (
    cancel_handler,
    get_achievements_handler,
    leaders_handler,
    start_handler,
)
from src.bot.handlers.error import error_handler
from src.bot.handlers.onboarding import choose_level_onboarding_handler, finish_onboarding_handler
from src.bot.handlers.payment import pre_checkout_handler, successful_payment_handler
from src.bot.handlers.questions import questions_handler
from src.bot.handlers.states import States
from src.utils.logging.logger import init_logger


def create_bot() -> Application:
    init_logger()

    pg_settings = PostgresSettings()
    persistence = PostgresPersistence(url=pg_settings.url_for_persistence)
    bot = Application.builder().token(bot_settings.TOKEN).persistence(persistence).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            States.onboarding: [
                CallbackQueryHandler(choose_level_onboarding_handler)
            ],
            States.finish_onboarding: [
                CallbackQueryHandler(finish_onboarding_handler)
            ],
            States.daily_question: [
                CallbackQueryHandler(questions_handler),
                CommandHandler('level', choose_level_command)
            ],
            States.change_level: [
                CallbackQueryHandler(change_level_handler),
            ],
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
    bot.add_handler(CommandHandler('achievements', get_achievements_handler))
    bot.add_handler(CommandHandler('level', choose_level_command))

    bot.add_handler(PreCheckoutQueryHandler(pre_checkout_handler))
    bot.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_handler))

    return bot
