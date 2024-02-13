import logging

from telegram import Update
from telegram import User as TGUser, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from telegram.ext import ContextTypes

from bot.handlers.states import States
from src.images import ImageType
from src.services.leaders import LeadersService
from src.services.users import UsersService
from src.services.coding_questions import CodingQuestionsService
from src.texts import GREETING_TEXT, START_BUTTON_TEXT
from src.utils.formaters import format_leaders_message
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.send_message import send_message
from settings import WEB_APP_URL

logger = logging.getLogger(__name__)


def _get_deep_link_param(update: Update) -> str | None:
    if not update.message:
        return

    if not update.message.text:
        return

    parts = update.message.text.split('/start ')
    if len(parts) >= 2:
        return parts[1]


async def start_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    users_service = UsersService(pg_pool=pg_pool)

    came_from = _get_deep_link_param(update=update)
    tg_user: TGUser = update.message.from_user
    user = await users_service.get_or_create(tg_user=tg_user, came_from=came_from)
    await users_service.set_status(user_id=user.id, status='active')
    logger.info(f'User %d run start handler', user.id)

    await send_message(
        message=update.message, text=GREETING_TEXT, choices=[START_BUTTON_TEXT], image=ImageType.greeting
    )
    return States.onboarding


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def leaders_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    leaders_service = LeadersService(pg_pool=pg_pool)
    users_service = UsersService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user = await users_service.get_or_create(tg_user=tg_user)
    logger.info(f'User %d run leaders handler', user.id)

    leaders = await leaders_service.get_top_users(limit=3)
    if not leaders:
        # TODO: add logging
        return States.daily_question

    user_in_leaders = await leaders_service.get_user_in_leaders(user_id=user.id)

    message_text = format_leaders_message(
        leaders=leaders,
        user_in_leaders=user_in_leaders
    )

    await send_message(message=update.message, text=message_text)
    return States.daily_question


async def set_difficult_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    # TODO: rewrite texts

    users_service = UsersService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user = await users_service.get_or_create(tg_user=tg_user)
    logger.info(f'User %d run difficult handler', user.id)

    if user.level == 2:
        await send_message(
            message=update.message, text='Вам уже и так приходят сложные вопросы'
        )
        return States.daily_question

    await users_service.set_level(user_id=user.id, level=2)
    await send_message(message=update.message, text='Теперь вопросы станут сложнее')
    return States.onboarding


async def set_easy_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    # TODO: rewrite texts

    users_service = UsersService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user = await users_service.get_or_create(tg_user=tg_user)
    logger.info(f'User %d run easy handler', user.id)

    if user.level == 1:
        await send_message(
            message=update.message, text='Вам уже и так приходят простые вопросы'
        )
        return States.daily_question

    await users_service.set_level(user_id=user.id, level=1)
    await send_message(message=update.message, text='Теперь вопросы станут легче')
    return States.daily_question


async def code_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    users_service = UsersService(pg_pool=pg_pool)
    coding_questions_service = CodingQuestionsService(pg_pool=pg_pool)

    tg_user: TGUser = update.message.from_user
    user = await users_service.get_or_create(tg_user=tg_user)
    logger.info(f'User %d run code handler', user.id)

    coding_question = await coding_questions_service.get_random_coding_question(user_id=user.id, user_level=user.level)

    url = WEB_APP_URL.format(question_id=coding_question.id, return_type=coding_question.return_type)

    await update.message.reply_text(
        text='Нажмите кнопку, чтобы начать',
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text='Начать',
                web_app=WebAppInfo(url=url)
            )
        )
    )
    return States.code
