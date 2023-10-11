import asyncio
import logging

import asyncpg
from telegram.ext import Application

from settings import BotSettings
from src.services.questions import QuestionsService
from src.services.users import User, UsersService
from src.utils.paywall import is_need_to_send_payment, is_passed_paywall
from src.utils.telegram.send_message import send_payment, send_question


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('ptbcontrib').setLevel(logging.WARNING)


logger = logging.getLogger(__name__)


async def send_daily_questions_task(pg_pool: asyncpg.Pool) -> None:
    bot_settings = BotSettings()
    bot = Application.builder().token(bot_settings.TOKEN).build().bot

    users_service = UsersService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    users: list[User] = await users_service.get_all()
    for user in users:
        if not is_passed_paywall(user=user):
            if not is_need_to_send_payment(user=user):
                continue

            is_payment_sent = await send_payment(bot=bot, chat_id=user.telegram_id, telegram_user_id=user.telegram_id)
            if is_payment_sent:
                await users_service.set_send_payment_at(user_id=user.id)
                logger.info(f'Send payment to user: {user.id}')
            else:
                logger.info(f'Can not send payment to user: {user.id}')
            continue

        question = await questions_service.get_new_random_question_for_user(user_id=user.id, user_level=user.level)

        if question:
            is_sent = await send_question(
                bot=bot,
                chat_id=user.telegram_id,
                question=question,
                questions_service=questions_service,
                user_id=user.id
            )
            if is_sent:
                await asyncio.sleep(0.1)
                logger.info(f'Send daily questions to user: {user.id}')
