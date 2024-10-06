import asyncio
import logging
import random

import asyncpg
from telegram.ext import Application

from settings import bot_settings
from src.services.questions import QuestionsService
from src.services.users import User, UsersService
from src.texts import NEW_QUESTION_FOR_YOU_TEXTS, SOLVE_QUESTIONS_BUTTON_TEXT
from src.utils.payment import PaymentInfo, get_payment_info
from src.utils.telegram.inline_keyboard import KeyboardButtonForFormatting
from src.utils.telegram.send_message import send_message, send_payment

logger = logging.getLogger(__name__)


async def send_daily_questions_task(pg_pool: asyncpg.Pool) -> None:
    bot = Application.builder().token(bot_settings.TOKEN).build().bot

    users_service = UsersService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    users: list[User] = await users_service.get_all()
    for user in users:
        if user.status != 'active':
            continue

        payment_info: PaymentInfo = get_payment_info(user=user)
        if not payment_info.is_passed_paywall:
            if payment_info.is_need_to_send_payment:
                is_payment_sent = await send_payment(telegram_user_id=user.telegram_id, bot=bot)
                if is_payment_sent:
                    await users_service.set_send_payment_at(user_id=user.id)
            continue

        # check we can send new question to user
        is_can_send_question = await questions_service.can_send_question(user_id=user.id)
        if not is_can_send_question:
            continue

        is_sent = await send_message(
            bot=bot,
            chat_id=user.telegram_id,
            text=random.choice(NEW_QUESTION_FOR_YOU_TEXTS),
            keyboard_buttons=[
                KeyboardButtonForFormatting(
                    text=SOLVE_QUESTIONS_BUTTON_TEXT,
                    web_app_url=f'{bot_settings.WEB_APP_URL}/solve-question'
                )
            ]
        )

        if is_sent:
            logger.info('Question sent to user %d', user.id)
        else:
            await users_service.set_status(user_id=user.id, status='block_bot')
            logger.info('User %d blocked bot', user.id)
        await asyncio.sleep(0.1)
