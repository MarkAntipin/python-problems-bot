import logging

from telegram import (
    CallbackQuery,
    Update,
)
from telegram import User as TGUser
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.handlers.states import States
from src.services.onboarding_questions import OnboardingQuestion, OnboardingQuestionsService
from src.services.questions import Question, QuestionsService
from src.services.users import User, UsersService
from src.texts import ENOUGH_QUESTIONS_FOR_TODAY, ONBOARDING_FINISH_TEXT
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.callback_data import ParsedCallbackData, parse_callback_data
from src.utils.telegram.job_queue import create_send_questions_task
from src.utils.telegram.send_message import send_answer_explanation, send_message, send_question
from src.images import ImageType

logger = logging.getLogger(__name__)


async def _answer_question(
    query: CallbackQuery,
    user_id: int,
    questions_service: QuestionsService | OnboardingQuestionsService,
    callback_data: ParsedCallbackData,
) -> tuple[Question | OnboardingQuestion | None, bool | None]:
    question, is_correct = await questions_service.answer_question(
        question_id=callback_data.question_id,
        user_id=user_id,
        user_answer=callback_data.answer
    )
    if question:
        await query.edit_message_text(
            parse_mode=ParseMode.HTML,
            text=(
                f"{question.text}\n\n"
                f"{callback_data.answer}) {question.choices[callback_data.answer]}"
            )
        )
    return question, is_correct


async def _send_daily_questions_task(context: ContextTypes.DEFAULT_TYPE) -> str | None:
    users_service = UsersService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    user_id = context.job.data
    user: User = await users_service.get_by_id(user_id=user_id)

    question = await questions_service.get_new_random_question_for_user(user_id=user.id, user_level=user.level)
    if question:
        await send_question(bot=context.bot, chat_id=context.job.chat_id, question=question)

    return States.daily_question


async def _send_daily_question_or_enough_questions_for_today(
    query: CallbackQuery,
    context: ContextTypes.DEFAULT_TYPE,
    questions_service: QuestionsService,
    user_id: int,
    user_level: int,
) -> None:
    question = await questions_service.get_new_random_question_for_user(user_id=user_id, user_level=user_level)
    if not question:
        await send_message(message=query.message, text=ENOUGH_QUESTIONS_FOR_TODAY)
        await create_send_questions_task(
            context=context,
            task=_send_daily_questions_task,
            chat_id=query.message.chat_id,
            user_id=user_id
        )
        return
    await send_question(message=query.message, question=question)


async def questions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    users_service = UsersService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    query = update.callback_query
    await query.answer()

    tg_user: TGUser = update.effective_user
    user: User = await users_service.get_or_create(tg_user=tg_user)

    if not user.level:
        logger.error("user: %d has no level", user.id)
        user_level = await users_service.set_level(user_id=user.id)
    else:
        user_level = user.level

    callback_data: ParsedCallbackData = parse_callback_data(callback_data=query.data)
    if callback_data:
        question, is_correct = await _answer_question(
            query=query, questions_service=questions_service, user_id=user.id, callback_data=callback_data
        )
        await send_answer_explanation(message=query.message, question=question, is_correct=is_correct)

    await _send_daily_question_or_enough_questions_for_today(
        query=query, questions_service=questions_service, user_id=user.id, user_level=user_level, context=context
    )
    return States.daily_question


async def onboarding_questions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    users_service = UsersService(pg_pool=pg_pool)
    onboarding_questions_service = OnboardingQuestionsService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup()

    tg_user: TGUser = query.from_user
    user: User = await users_service.get_or_create(tg_user=tg_user)

    callback_data = parse_callback_data(callback_data=query.data)
    if callback_data:
        await _answer_question(
            query=query, questions_service=onboarding_questions_service, user_id=user.id, callback_data=callback_data
        )

    onboarding_question = await onboarding_questions_service.get_new_question_for_user(user_id=user.id)
    if not onboarding_question:
        user_level = await users_service.set_level(user_id=user.id)
        await send_message(message=query.message, text=ONBOARDING_FINISH_TEXT, image=ImageType.onboarding_finish)

        await _send_daily_question_or_enough_questions_for_today(
            query=query, questions_service=questions_service, user_id=user.id, user_level=user_level, context=context
        )
        return States.daily_question

    await send_question(message=query.message, question=onboarding_question)
    return States.onboarding_question
