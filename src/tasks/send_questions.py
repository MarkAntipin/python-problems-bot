import asyncio
import logging

import asyncpg
from telegram.ext import Application

from settings import bot_settings
from src.services.questions import GetNewRandomQuestionForUserStatus, QuestionsService
from src.services.users import User, UsersService
from src.utils.telegram.send_message import send_question

logger = logging.getLogger(__name__)


async def send_daily_questions_task(pg_pool: asyncpg.Pool) -> None:
    bot = Application.builder().token(bot_settings.TOKEN).build().bot

    users_service = UsersService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    users: list[User] = await users_service.get_all()
    for user in users:
        if user.status != 'active':
            continue

        new_question_resp = await questions_service.get_new_random_question_for_user(
            user_id=user.id, user_level=user.level
        )
        if not new_question_resp.status == GetNewRandomQuestionForUserStatus.ok:
            continue

        is_sent = await send_question(
            bot=bot,
            chat_id=user.telegram_id,
            question=new_question_resp.question,
            questions_service=questions_service,
            user_id=user.id
        )
        if is_sent:
            logger.info('Question sent to user %d', user.id)
        else:
            await users_service.set_status(user_id=user.id, status='block_bot')
            logger.info('User %d blocked bot', user.id)
        await asyncio.sleep(0.1)
