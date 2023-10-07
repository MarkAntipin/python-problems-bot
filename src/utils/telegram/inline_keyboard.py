from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils.telegram.callback_data import format_callback_data_for_question


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
