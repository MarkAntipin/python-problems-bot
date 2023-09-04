import logging

from telegram import (
    Message,
)
from telegram.ext import ContextTypes

from bot.handlers.states import States
from src.services.questions import QuestionsService
from src.services.users import User, UsersService
from src.texts import (
    ENOUGH_QUESTIONS_FOR_TODAY,
    WE_WILL_SEND_YOU_QUESTIONS_SOON,
)
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.job_queue import create_send_questions_task
from src.utils.telegram.send_message import send_message, send_question

logger = logging.getLogger(__name__)


async def _send_daily_questions_task(context: ContextTypes.DEFAULT_TYPE) -> str | None:
    users_service = UsersService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    user_id = context.job.data
    user: User = await users_service.get_by_id(user_id=user_id)

    question = await questions_service.get_new_random_question_for_user(user_id=user.id, user_level=user.level)
    if question:
        await send_question(bot=context.bot, chat_id=context.job.chat_id, question=question)

    return States.daily_question


async def send_daily_question_or_enough_questions_for_today(
    message: Message,
    context: ContextTypes.DEFAULT_TYPE,
    questions_service: QuestionsService,
    user_id: int,
    user_level: int,
    is_main_flow: bool = True
) -> None:
    question = await questions_service.get_new_random_question_for_user(user_id=user_id, user_level=user_level)
    is_added = await create_send_questions_task(
        context=context,
        task=_send_daily_questions_task,
        chat_id=message.chat_id,
        user_id=user_id
    )
    if is_added:
        logger.info('User %d, added to queue', user_id)

    if not question:
        await send_message(message=message, text=ENOUGH_QUESTIONS_FOR_TODAY)
        return

    if is_added is False and is_main_flow is False:
        logger.error('User %d, trying to get more questions', user_id)
        await send_message(message=message, text=WE_WILL_SEND_YOU_QUESTIONS_SOON)
        return

    # TODO: in transaction
    await questions_service.send_question(user_id=user_id, question_id=question.id)
    await send_question(message=message, question=question)
