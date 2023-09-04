import pathlib

from telegram import Bot, InlineKeyboardMarkup, Message, ReplyKeyboardRemove
from telegram.constants import ParseMode

from src.images import IMAGE_TYPE_TO_IMAGE_PATH, ImageType
from src.services.onboarding_questions import OnboardingQuestion
from src.services.questions import Question
from src.texts import CORRECT_ANSWER_TEXT, INCORRECT_ANSWER_TEXT
from src.utils.telegram.inline_keyboard import (
    format_choices,
    format_inline_keyboard,
    format_inline_keyboard_for_question,
)


async def _send_message(
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    message: Message | None = None,
    bot: Bot | None = None,
    chat_id: int | None = None,
    photo_path: pathlib.Path = None
) -> None:
    if not message and not bot:
        raise ValueError('message or bot should be passed to send message')

    if not reply_markup:
        reply_markup = ReplyKeyboardRemove()
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
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup,
        )


async def send_message(
    text: str,
    choices: list[str] | None = None,
    message: Message | None = None,
    bot: Bot | None = None,
    chat_id: int | None = None,
    image: ImageType | None = None
) -> None:
    await _send_message(
        message=message,
        bot=bot,
        chat_id=chat_id,
        text=text,
        reply_markup=format_inline_keyboard(choices=choices) if choices else None,
        photo_path=IMAGE_TYPE_TO_IMAGE_PATH.get(image) or None
    )


async def send_question(
    question: Question | OnboardingQuestion,
    message: Message | None = None,
    bot: Bot | None = None,
    chat_id: int | None = None
) -> None:
    formatted_choices = format_choices(choices=question.choices)
    text = f'{question.text}\n\n{formatted_choices}'
    reply_markup = format_inline_keyboard_for_question(choices=question.choices, question_id=question.id)
    await _send_message(
        message=message,
        bot=bot,
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
    )


async def send_answer_explanation(
    question: Question,
    is_correct: bool,
    message: Message | None = None,
) -> None:
    if is_correct:
        answer_text = CORRECT_ANSWER_TEXT
    else:
        answer_text = INCORRECT_ANSWER_TEXT

    await _send_message(
        message=message,
        text=f'{answer_text}{question.explanation}' if question.explanation else answer_text
    )
