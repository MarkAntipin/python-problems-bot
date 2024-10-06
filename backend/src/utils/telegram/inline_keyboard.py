from pydantic import BaseModel

from src.utils.telegram.callback_data import format_callback_data_for_question
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.error import BadRequest


class KeyboardButtonForFormatting(BaseModel):
    text: str
    web_app_url: str | None = None


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


def format_inline_keyboard(keyboard_buttons: list[KeyboardButtonForFormatting]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(
                keyboard_button.text,
                callback_data=i if not keyboard_button.web_app_url else None,
                web_app=WebAppInfo(url=keyboard_button.web_app_url) if keyboard_button.web_app_url else None
            )]
            for i, keyboard_button in enumerate(keyboard_buttons, start=1)
        ]
    )


async def remove_inline_keyboard(query: CallbackQuery) -> None:
    try:
        await query.edit_message_reply_markup()
    except BadRequest:
        pass
