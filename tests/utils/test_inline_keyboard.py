from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils.telegram.inline_keyboard import format_inline_keyboard, format_inline_keyboard_for_question


def test_format_inline_keyboard() -> None:
    res = format_inline_keyboard(
        choices=['A', 'B', 'C']
    )
    assert res == InlineKeyboardMarkup(
        inline_keyboard=((
            InlineKeyboardButton(callback_data=1, text='A'),
            InlineKeyboardButton(callback_data=2, text='B'),
            InlineKeyboardButton(callback_data=3, text='C')),
        )
    )


def test_format_inline_keyboard_for_question() -> None:
    res = format_inline_keyboard_for_question(
        choices={'A': 1, 'B': 2, 'C': 3},
        question_id=1
    )
    assert res == InlineKeyboardMarkup(
        inline_keyboard=((
            InlineKeyboardButton(callback_data='A_1', text='A'),
            InlineKeyboardButton(callback_data='B_1', text='B'),
            InlineKeyboardButton(callback_data='C_1', text='C')),
        )
    )
