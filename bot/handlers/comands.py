import logging

from telegram import Update
from telegram import User as TGUser
from telegram.ext import ContextTypes

from bot.handlers.states import States
from src.images import ImageType
from src.services.onboarding_questions import OnboardingQuestionsService
from src.services.questions import QuestionsService
from src.services.users import User, UsersService
from src.texts import GREETING_TEXT, ONBOARDING_START_BUTTON_TEXT, ONBOARDING_START_TEXT
from src.utils.common import send_daily_question_or_enough_questions_for_today
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.send_message import send_message

logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    users_service = UsersService(pg_pool=pg_pool)
    onboarding_questions_service = OnboardingQuestionsService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user: User = await users_service.get_or_create(tg_user=tg_user)
    if user.level:
        logger.error("user: %d already has level", user.id)
        await send_daily_question_or_enough_questions_for_today(
            message=update.message,
            context=context,
            user_id=user.id,
            user_level=user.level,
            questions_service=questions_service,
            is_main_flow=False
        )
        return States.daily_question

    if not await onboarding_questions_service.get_new_question_for_user(user_id=user.id):
        logger.error("user: %d doesn't have any onboarding questions", user.id)
        user_level = await users_service.set_level(user_id=user.id)
        await send_daily_question_or_enough_questions_for_today(
            message=update.message,
            context=context,
            user_id=user.id,
            user_level=user_level,
            questions_service=questions_service,
            is_main_flow=False
        )
        return States.daily_question

    await send_message(message=update.message, text=GREETING_TEXT, image=ImageType.greeting)
    await send_message(
        message=update.message,
        text=ONBOARDING_START_TEXT,
        choices=[ONBOARDING_START_BUTTON_TEXT],
        image=ImageType.onboarding_start
    )
    return States.onboarding_question


async def cansel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass
