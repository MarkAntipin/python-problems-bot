import logging

from telegram import Update
from telegram import User as TGUser
from telegram.ext import ContextTypes

from bot.handlers.states import States
from src.images import ImageType
from src.services.leaders import LeadersService
from src.services.users import UsersService
from src.texts import GREETING_TEXT, START_BUTTON_TEXT
from src.utils.formaters import format_leaders_message
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.send_message import send_message

logger = logging.getLogger(__name__)


def _get_deep_link_param(update: Update) -> str | None:
    if not update.message:
        return

    if not update.message.text:
        return

    parts = update.message.text.split('/start ')
    if len(parts) >= 2:
        return parts[1]


async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    users_service = UsersService(pg_pool=pg_pool)

    came_from = _get_deep_link_param(update=update)
    tg_user: TGUser = update.message.from_user
    await users_service.get_or_create(tg_user=tg_user, came_from=came_from)

    await send_message(
        message=update.message, text=GREETING_TEXT, choices=[START_BUTTON_TEXT], image=ImageType.greeting
    )
    return States.onboarding


async def cansel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def leaders_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    leaders_service = LeadersService(pg_pool=pg_pool)
    users_service = UsersService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user = await users_service.get_or_create(tg_user=tg_user)

    leaders = await leaders_service.get_top_users(limit=3)
    if not leaders:
        # TODO: add logging
        return States.daily_question

    user_in_leaders = await leaders_service.get_user_in_leaders(user_id=user.id)

    message_text = format_leaders_message(
        leaders=leaders,
        user_in_leaders=user_in_leaders
    )

    await send_message(message=update.message, text=message_text)
    return States.daily_question


async def set_difficult_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    # TODO: rewrite texts

    users_service = UsersService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user = await users_service.get_or_create(tg_user=tg_user)

    if user.level == 2:
        await send_message(
            message=update.message, text='Вам уже и так приходят сложные вопросы'
        )
        return States.daily_question

    await users_service.set_level(user_id=user.id, level=2)
    await send_message(message=update.message, text='Теперь вопросы станут сложнее')
    return States.onboarding


async def set_easy_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    # TODO: rewrite texts

    users_service = UsersService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user = await users_service.get_or_create(tg_user=tg_user)

    if user.level == 1:
        await send_message(
            message=update.message, text='Вам уже и так приходят простые вопросы'
        )
        return States.daily_question

    await users_service.set_level(user_id=user.id, level=1)
    await send_message(message=update.message, text='Теперь вопросы станут легче')
    return States.daily_question
