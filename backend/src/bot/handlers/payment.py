import logging

from telegram import Update
from telegram import User as TGUser
from telegram.ext import (
    ContextTypes,
)

from settings import bot_settings
from src.images import ImageType
from src.mappers.users import map_inner_telegram_user_from_tg_user
from src.services.questions import QuestionsService
from src.services.users import UsersService
from src.texts import (
    SOLVE_QUESTIONS_BUTTON_TEXT,
    THANK_YOU_FOR_PAYMENT_CAN_FIND_QUESTION_TEXT,
    THANK_YOU_FOR_PAYMENT_CAN_NOT_FIND_QUESTION_TEXT,
)
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.inline_keyboard import KeyboardButtonForFormatting
from src.utils.telegram.send_message import send_message

logger = logging.getLogger(__name__)


async def pre_checkout_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query
    users_service = UsersService(pg_pool=pg_pool)
    tg_user: TGUser = update.effective_user
    user, _ = await users_service.get_or_create(tg_user=map_inner_telegram_user_from_tg_user(tg_user))

    if email := query.order_info.email:
        await users_service.set_email(user_id=user.id, email=email)
    logger.info('User %d trying to process payment', user.id)
    await query.answer(ok=True)


async def successful_payment_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    users_service = UsersService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    tg_user: TGUser = update.effective_user
    user, _ = await users_service.get_or_create(tg_user=map_inner_telegram_user_from_tg_user(tg_user))

    await users_service.set_paid_status(user_id=user.id)
    logger.info('User %d paid', user.id)

    # check we can send new question to user
    is_can_send_question = await questions_service.can_send_question(user_id=user.id)
    if is_can_send_question:
        text = THANK_YOU_FOR_PAYMENT_CAN_FIND_QUESTION_TEXT
        keyboard_buttons = [
            KeyboardButtonForFormatting(
                text=SOLVE_QUESTIONS_BUTTON_TEXT,
                web_app_url=f'{bot_settings.WEB_APP_URL}/solve-question'
            )
        ]
    else:
        text = THANK_YOU_FOR_PAYMENT_CAN_NOT_FIND_QUESTION_TEXT
        keyboard_buttons = []

    await send_message(
        message=update.message,
        text=text,
        image=ImageType.thank_you,
        keyboard_buttons=keyboard_buttons
    )
