import logging
import random
from asyncio import sleep

from telegram import (
    Update,
)
from telegram import User as TGUser
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from settings import bot_settings
from src.bot.handlers.states import States
from src.services.achievements import Achievement, AchievementsService
from src.services.models.payment_status import PaymentStatus
from src.services.questions import GetNewRandomQuestionForUserStatus, QuestionsService
from src.services.users import User, UsersService
from src.texts import ENOUGH_QUESTIONS_FOR_TODAY_TEXTS, NO_MORE_QUESTIONS_TEXT
from src.utils.formaters import format_achievement, format_explanation
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.callback_data import ParsedCallbackQuestionsData, parse_callback_questions_data
from src.utils.telegram.send_message import send_message, send_question

logger = logging.getLogger(__name__)


async def questions_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    users_service = UsersService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)
    achievements_service = AchievementsService(pg_pool=pg_pool)

    query = update.callback_query
    await query.answer()
    try:
        # TODO: why errors here?
        await query.edit_message_reply_markup()
    except BadRequest as e:
        logger.error(e, exc_info=True)

    tg_user: TGUser = update.effective_user
    user: User = await users_service.get_or_create(tg_user=tg_user)

    if user.payment_status == PaymentStatus.onboarding:
        user = await users_service.set_trial_status(user_id=user.id)

    callback_questions_data: ParsedCallbackQuestionsData = parse_callback_questions_data(callback_data=query.data)
    if callback_questions_data:
        # answer on previous question
        user_answer = callback_questions_data.answer
        previous_question = await questions_service.get_by_id(question_id=callback_questions_data.question_id)
        if not previous_question:
            logger.error('No question found to answer. question_id: %d', callback_questions_data.question_id)
        else:
            is_correct = await questions_service.answer_question(
                question=previous_question,
                user_id=user.id,
                user_answer=user_answer
            )

            await query.edit_message_text(
                parse_mode=ParseMode.MARKDOWN_V2,
                text=format_explanation(
                    question=previous_question,
                    is_correct=is_correct,
                    user_answer=user_answer
                )
            )
            achievements: list[Achievement] | None = await achievements_service.check_for_new_achievements(
                user_id=user.id
            )
            if achievements:
                for achievement in achievements:
                    await send_message(
                        message=query.message,
                        text=format_achievement(achievement=achievement)
                    )
                    await send_message(
                        message=query.message,
                        text=achievement.emoji
                    )
                    # TODO: do we need delay here?
                    await sleep(bot_settings.DELAY_AFTER_ACHIEVEMENT)

    # send new question
    new_question_resp = await questions_service.get_new_random_question_for_user(user_id=user.id, user_level=user.level)

    if new_question_resp.status == GetNewRandomQuestionForUserStatus.no_questions_for_today:
        await send_message(message=query.message, text=random.choice(ENOUGH_QUESTIONS_FOR_TODAY_TEXTS))
        return States.daily_question

    if new_question_resp.status == GetNewRandomQuestionForUserStatus.no_more_questions:
        await send_message(message=query.message, text=NO_MORE_QUESTIONS_TEXT)
        return States.daily_question

    await send_question(
        message=query.message,
        question=new_question_resp.question,
        questions_service=questions_service,
        user_id=user.id
    )
    return States.daily_question
