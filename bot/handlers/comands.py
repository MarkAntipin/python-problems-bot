import logging

from telegram import Update
from telegram import User as TGUser
from telegram.ext import ContextTypes

from bot.handlers.states import States
from src.images import ImageType
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
