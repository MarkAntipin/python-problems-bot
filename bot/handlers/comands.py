import logging

from telegram import Update
from telegram import User as TGUser
from telegram.ext import ContextTypes

from bot.handlers.states import States
from src.images import ImageType
from src.repositories.postgres.users import UsersRepo
from src.services.users import UsersService
from src.texts import GREETING_TEXT, START_BUTTON_TEXT
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


async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str | None:
    users_service = UsersService(pg_pool=pg_pool)

    came_from = _get_deep_link_param(update=update)
    tg_user: TGUser = update.message.from_user
    await users_service.get_or_create(tg_user=tg_user, came_from=came_from)

    await send_message(
        message=update.message, text=GREETING_TEXT, choices=[START_BUTTON_TEXT], image=ImageType.greeting
    )
    return States.daily_question


async def cansel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass

async def leaders_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    users_repo = UsersRepo(pg_pool=pg_pool)

    leaders = await users_repo.get_top_users(limit=3)

    tg_user = update.message.from_user
    user_position = await users_repo.get_user_position(tg_user=tg_user)
    user_score = await users_repo.get_user_score(tg_user=tg_user)

    message_text = 'Таблица лидеров:\n'
    for i, leader in enumerate(leaders, start=1):
        message_text += f"{i}. {leader['first_name']} - {leader['score']} баллов\n"

    message_text += f"\nВаше текущее место: {user_position}. Вы набрали {user_score} баллов."

    await send_message(message=update.message, text=message_text)
