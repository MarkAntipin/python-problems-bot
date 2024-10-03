import logging

from telegram import Update
from telegram import User as TGUser
from telegram.ext import ContextTypes

from settings import bot_settings
from src.images import ImageType
from src.mappers.users import map_inner_telegram_user_from_tg_user
from src.services.users import UsersService
from src.texts import CHANGE_LEVEL_BUTTON_TEXT, GREETING_TEXT, START_BUTTON_TEXT
from src.utils.payment import PaymentInfo, get_payment_info
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.inline_keyboard import KeyboardButtonForFormatting
from src.utils.telegram.send_message import send_message, send_payment

logger = logging.getLogger(__name__)


def _get_deep_link_param(update: Update) -> str | None:
    if not update.message:
        return

    if not update.message.text:
        return

    parts = update.message.text.split('/start ')
    if len(parts) >= 2:
        return parts[1]


async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    came_from: str | None = _get_deep_link_param(update=update)

    users_service = UsersService(pg_pool=pg_pool)
    tg_user: TGUser = update.message.from_user
    user, is_created = await users_service.get_or_create(
        tg_user=map_inner_telegram_user_from_tg_user(tg_user), came_from=came_from
    )

    payment_info: PaymentInfo = get_payment_info(user=user)
    if not payment_info.is_passed_paywall:
        await send_payment(message=update.message, telegram_user_id=user.telegram_id)
        return

    keyboard_buttons = [
        KeyboardButtonForFormatting(
            text=START_BUTTON_TEXT,
            web_app_url=(
                f'{bot_settings.WEB_APP_URL}/choose-level'
                if is_created else f'{bot_settings.WEB_APP_URL}/solve-question'
            )
        ),
    ]

    # if it is an old user, he can change level
    if not is_created:
        keyboard_buttons.insert(
            0,
            KeyboardButtonForFormatting(
                text=CHANGE_LEVEL_BUTTON_TEXT,
                web_app_url=f'{bot_settings.WEB_APP_URL}/choose-level'
            )
        )

    await send_message(
        message=update.message,
        text=GREETING_TEXT,
        keyboard_buttons=keyboard_buttons,
        image=ImageType.greeting
    )


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass
