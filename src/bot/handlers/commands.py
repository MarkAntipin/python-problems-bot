import logging

from telegram import Update
from telegram import User as TGUser
from telegram.ext import ContextTypes

from src.bot.handlers.states import States
from src.images import ImageType
from src.services.achievements import AchievementsService
from src.services.leaders import LeadersService
from src.services.users import UsersService
from src.texts import GREETING_TEXT, START_BUTTON_TEXT
from src.utils.formaters import format_achievements_list, format_leaders_message
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
    user = await users_service.get_or_create(tg_user=tg_user, came_from=came_from)
    await users_service.set_status(user_id=user.id, status='active')
    logger.info('User %d run start handler', user.id)

    await send_message(
        message=update.message, text=GREETING_TEXT, choices=[START_BUTTON_TEXT], image=ImageType.greeting
    )
    return States.onboarding


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def leaders_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    leaders_service = LeadersService(pg_pool=pg_pool)
    users_service = UsersService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user = await users_service.get_or_create(tg_user=tg_user)
    logger.info('User %d run leaders handler', user.id)

    leaders = await leaders_service.get_top_users(limit=5)
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


async def get_achievements_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    users_service = UsersService(pg_pool=pg_pool)
    achievements_service = AchievementsService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user = await users_service.get_or_create(tg_user=tg_user)
    logger.info('User %d run achievements handler', user.id)

    achievements = await achievements_service.get_user_achievements(user_id=user.id)
    await send_message(
        message=update.message, text=format_achievements_list(achievements=achievements)
    )
    return States.daily_question
