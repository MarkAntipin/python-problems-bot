import logging

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from bot.handlers.states import States
from src.texts import CHOOSE_LEVEL_TEXT, FINISH_ONBOARDING_TEXT
from src.utils.telegram.send_message import send_message
from src.services.users import User, UsersService
from src.utils.postgres_pool import pg_pool
from telegram import User as TGUser


logger = logging.getLogger(__name__)


async def choose_level_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query

    await query.answer()
    try:
        # TODO: why errors here?
        await query.edit_message_reply_markup()
    except BadRequest as e:
        logger.error(e, exc_info=True)

    await send_message(
        message=query.message,
        text=CHOOSE_LEVEL_TEXT,
        choices=['👶', '👨‍🎓'],
    )
    return States.finish_onboarding


async def finish_onboarding_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query

    await query.answer()
    try:
        # TODO: why errors here?
        await query.edit_message_reply_markup()
    except BadRequest as e:
        logger.error(e, exc_info=True)

    users_service = UsersService(pg_pool=pg_pool)
    tg_user: TGUser = update.effective_user
    user: User = await users_service.get_or_create(tg_user=tg_user)

    if query.data and query.data.isdigit():
        level = int(query.data)
        await users_service.set_level(user_id=user.id, level=level)

    # TODO: rewrite texts
    await send_message(
        message=query.message,
        text=FINISH_ONBOARDING_TEXT,
        choices=['К задачам!'],
    )
    return States.daily_question
