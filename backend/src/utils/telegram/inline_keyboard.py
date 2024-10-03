from src.utils.telegram.callback_data import format_callback_data_for_question
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest


def format_inline_keyboard_for_question(choices: dict, question_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    choice,
                    callback_data=format_callback_data_for_question(choice=choice, question_id=question_id)
                ) for choice in choices.keys()
            ]
        ]
    )


def format_inline_keyboard(choices: list[str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(choice, callback_data=i) for i, choice in enumerate(
        choices, start=1
    )]])


async def remove_inline_keyboard(query: CallbackQuery) -> None:
    try:
        await query.edit_message_reply_markup()
    except BadRequest:
        pass
