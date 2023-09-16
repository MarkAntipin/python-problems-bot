from src.utils.telegram.inline_keyboard import format_inline_keyboard, format_inline_keyboard_for_question
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def test_format_inline_keyboard():
    res = format_inline_keyboard(
        choices=['A', 'B', 'C']
    )
    assert res == InlineKeyboardMarkup(
        inline_keyboard=((
            InlineKeyboardButton(callback_data=0, text='A'),
            InlineKeyboardButton(callback_data=1, text='B'),
            InlineKeyboardButton(callback_data=2, text='C')),
        )
    )


def test_format_inline_keyboard_for_question():
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
