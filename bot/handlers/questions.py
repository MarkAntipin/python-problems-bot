import logging

from telegram import (
    CallbackQuery,
    Update,
)
from telegram import User as TGUser
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.handlers.states import States
from src.images import ImageType
from src.services.onboarding_questions import OnboardingQuestionsService
from src.services.questions import QuestionsService
from src.services.users import User, UsersService
from src.texts import CORRECT_ANSWER_TEXT, INCORRECT_ANSWER_TEXT, ONBOARDING_FINISH_TEXT
from src.utils.common import send_daily_question_or_enough_questions_for_today
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.callback_data import ParsedCallbackData, parse_callback_data
from src.utils.telegram.send_message import send_message, send_question

logger = logging.getLogger(__name__)


async def _answer_daily_question(
    query: CallbackQuery,
    user_id: int,
    questions_service: QuestionsService,
    callback_data: ParsedCallbackData,
) -> None:
    question = await questions_service.get_by_id(question_id=callback_data.question_id)
    if not question:
        logger.error('No question found to answer. question_id: %d', callback_data.question_id)
        return

    is_correct = await questions_service.answer_question(
        question=question,
        user_id=user_id,
        user_answer=callback_data.answer
    )
    if is_correct:
        answer_text = CORRECT_ANSWER_TEXT
    else:
        answer_text = INCORRECT_ANSWER_TEXT

    text = (
        f"{question.text}\n\n"
        f"<b>Твой ответ:</b> {callback_data.answer}) {question.choices[callback_data.answer]}\n"
        f"<b>Правильный ответ:</b> {question.answer}) {question.choices[question.answer]}\n\n"
        f"{answer_text}{question.explanation}"
    )

    await query.edit_message_text(
        parse_mode=ParseMode.HTML,
        text=text
    )


async def _answer_onboarding_question(
        query: CallbackQuery,
        user_id: int,
        onboarding_questions_service: OnboardingQuestionsService,
        callback_data: ParsedCallbackData,
) -> None:
    onboarding_question = await onboarding_questions_service.get_by_id(question_id=callback_data.question_id)
    if not onboarding_question:
        logger.error('No question found to answer. question_id: %d', callback_data.question_id)
        return

    await onboarding_questions_service.answer_question(
        question=onboarding_question,
        user_id=user_id,
        user_answer=callback_data.answer
    )

    text = (
        f"{onboarding_question.text}\n\n"
        f"{callback_data.answer}) {onboarding_question.choices[callback_data.answer]}"
    )

    await query.edit_message_text(
        parse_mode=ParseMode.HTML,
        text=text
    )


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
        await _answer_daily_question(
            query=query, questions_service=questions_service, user_id=user.id, callback_data=callback_data
        )

    await send_daily_question_or_enough_questions_for_today(
        message=query.message,
        questions_service=questions_service,
        user_id=user.id,
        user_level=user_level,
        context=context
    )
    return States.daily_question


async def onboarding_questions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    users_service = UsersService(pg_pool=pg_pool)
    onboarding_questions_service = OnboardingQuestionsService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    query = update.callback_query
    await query.answer()
    # await query.edit_message_reply_markup()

    tg_user: TGUser = query.from_user
    user: User = await users_service.get_or_create(tg_user=tg_user)

    callback_data = parse_callback_data(callback_data=query.data)
    if callback_data:
        await _answer_onboarding_question(
            query=query,
            onboarding_questions_service=onboarding_questions_service,
            user_id=user.id,
            callback_data=callback_data
        )

    onboarding_question = await onboarding_questions_service.get_new_question_for_user(user_id=user.id)
    if not onboarding_question:
        user_level = await users_service.set_level(user_id=user.id)
        await send_message(message=query.message, text=ONBOARDING_FINISH_TEXT, image=ImageType.onboarding_finish)

        await send_daily_question_or_enough_questions_for_today(
            message=query.message,
            questions_service=questions_service,
            user_id=user.id,
            user_level=user_level,
            context=context
        )
        return States.daily_question

    # TODO: in transaction
    await onboarding_questions_service.send_question(user_id=user.id, question_id=onboarding_question.id)
    await send_question(message=query.message, question=onboarding_question)
    return States.onboarding_question
