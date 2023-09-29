import asyncio
import logging

import asyncpg
from telegram.ext import Application

from settings import BotSettings
from src.services.questions import QuestionsService
from src.services.users import User, UsersService
from src.utils.telegram.send_message import send_question

logger = logging.getLogger(__name__)


async def send_daily_questions_task(pg_pool: asyncpg.Pool) -> None:
    bot_settings = BotSettings()
    bot = Application.builder().token(bot_settings.TOKEN).build().bot

    users_service = UsersService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    users: list[User] = await users_service.get_all()
    for user in users:
        question = await questions_service.get_new_random_question_for_user(user_id=user.id)

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
