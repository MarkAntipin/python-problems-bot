import logging

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from bot.handlers.states import States
from src.utils.telegram.send_message import send_message

logger = logging.getLogger(__name__)


async def choose_level_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query

    await query.answer()
    try:
        # TODO: why errors here?
        await query.edit_message_reply_markup()
    except BadRequest as e:
        logger.error(e, exc_info=True)

    # TODO: rewrite texts
    await send_message(
        message=query.message,
        text=(
            """
Выбери свой уровень, отвечай честно!
👶 - я новичок в python, но готов ко всему!
👨‍🎓 - я уже знаю python. Моя цель - найти первую работу

Ты всегда сможешь изменить свой уровень командами:
/difficult - сделать посложнее
/easy - сделать полегче
            """
        ),
        choices=['👶', '👨‍🎓'],
    )
    return States.daily_question

