import logging

from telegram import (
    CallbackQuery,
    Update,
)
from telegram import User as TGUser
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.handlers.states import States
from src.services.questions import QuestionsService
from src.services.users import User, UsersService
from src.texts import CORRECT_ANSWER_TEXT, INCORRECT_ANSWER_TEXT
from src.utils.common import send_daily_question_or_enough_questions_for_today
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.callback_data import ParsedCallbackQuestionsData, parse_callback_questions_data

logger = logging.getLogger(__name__)


async def _answer_daily_question(
    query: CallbackQuery,
    user_id: int,
    questions_service: QuestionsService,
    callback_questions_data: ParsedCallbackQuestionsData,
) -> None:
    question_id: int = callback_questions_data.question_id
    user_answer: str = callback_questions_data.answer

    question = await questions_service.get_by_id(question_id=question_id)
    if not question:
        logger.error('No question found to answer. question_id: %d', question_id)
        return

    is_correct = await questions_service.answer_question(
        question=question,
        user_id=user_id,
        user_answer=user_answer
    )
    if is_correct:
        answer_text = CORRECT_ANSWER_TEXT
    else:
        answer_text = INCORRECT_ANSWER_TEXT

    text = (
        f"{question.text}\n\n"
        f"<b>Ответ:</b> {question.answer}) {question.choices[question.answer]}\n\n"
        f"{answer_text}"
        f"<b> Объяснение:</b>\n"
        f"{question.explanation}"
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
    await query.edit_message_reply_markup()

    tg_user: TGUser = update.effective_user
    user: User = await users_service.get_or_create(tg_user=tg_user)

    callback_questions_data: ParsedCallbackQuestionsData = parse_callback_questions_data(callback_data=query.data)
    if callback_questions_data:
        await _answer_daily_question(
            query=query,
            questions_service=questions_service,
            user_id=user.id,
            callback_questions_data=callback_questions_data
        )

    await send_daily_question_or_enough_questions_for_today(
        message=query.message,
        questions_service=questions_service,
        user_id=user.id,
        context=context
    )
    return States.daily_question
