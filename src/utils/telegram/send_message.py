import logging
import pathlib

from telegram import Bot, InlineKeyboardMarkup, Message, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.error import Forbidden

from src.images import IMAGE_TYPE_TO_IMAGE_PATH, ImageType
from src.services.questions import Question, QuestionsService
from src.services.advices import Advice, AdvicesService
from src.utils.formaters import format_question, format_advice
from src.utils.telegram.inline_keyboard import (
    format_inline_keyboard,
    format_inline_keyboard_for_question
)

logger = logging.getLogger(__name__)


async def _send_message(
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    message: Message | None = None,
    bot: Bot | None = None,
    chat_id: int | None = None,
    photo_path: pathlib.Path = None
) -> bool:
    if not message and not bot:
        raise ValueError('message or bot should be passed to send message')

    if not reply_markup:
        reply_markup = ReplyKeyboardRemove()
    try:
        if message:
            if photo_path:
                await message.reply_photo(
                    photo=photo_path,
                    caption=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                )
            else:
                await message.reply_text(
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                )
        elif bot:
            if photo_path:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_path,
                    caption=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                )
            else:
                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                )
    except Forbidden:
        logger.error('User has blocked bot')
        return False

    return True


async def send_message(
    text: str,
    choices: list[str] | None = None,
    message: Message | None = None,
    bot: Bot | None = None,
    chat_id: int | None = None,
    image: ImageType | None = None
) -> bool:
    return await _send_message(
        message=message,
        bot=bot,
        chat_id=chat_id,
        text=text,
        reply_markup=format_inline_keyboard(choices=choices) if choices else None,
        photo_path=IMAGE_TYPE_TO_IMAGE_PATH.get(image) or None
    )


async def send_question(
    question: Question,
    questions_service: QuestionsService,
    user_id: int,
    message: Message | None = None,
    bot: Bot | None = None,
    chat_id: int | None = None
) -> bool:
    reply_markup = format_inline_keyboard_for_question(
        choices=question.choices,
        question_id=question.id
    )
    is_sent = await _send_message(
        message=message,
        bot=bot,
        chat_id=chat_id,
        text=format_question(question=question),
        reply_markup=reply_markup,
    )
    if is_sent:
        await questions_service.send_question(user_id=user_id, question_id=question.id)
        logger.info('Send question to user %d', user_id)
    return is_sent


async def send_advice(
    advice: Advice,
    advices_service: AdvicesService,
    user_id: int,
    message: Message | None = None,
    bot: Bot | None = None,
    chat_id: int | None = None
) -> bool:
    is_sent = await _send_message(
        message=message,
        bot=bot,
        chat_id=chat_id,
        text=format_advice(advice=advice)
    )
    if is_sent:
        await advices_service.send_advice(user_id=user_id, advice_id=advice.advice_id)
        logger.info('Send advice to user %d', user_id)

    return is_sent
