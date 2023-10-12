import logging

from telegram import Update
from telegram import User as TGUser
from telegram.ext import (
    ContextTypes,
)

from bot.handlers.states import States
from src.images import ImageType
from src.services.questions import QuestionsService
from src.services.users import User, UsersService
from src.texts import THANK_YOU_FOR_PAYMENT_TEXT
from src.utils.postgres_pool import pg_pool
from src.utils.telegram.send_message import send_message, send_question

logger = logging.getLogger(__name__)


async def pre_checkout_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query
    users_service = UsersService(pg_pool=pg_pool)
    tg_user: TGUser = update.effective_user
    user: User = await users_service.get_or_create(tg_user=tg_user)

    if email := query.order_info.email:
        await users_service.set_email(user_id=user.id, email=email)
    logger.info('User %d trying to process payment', user.id)
    await query.answer(ok=True)


async def successful_payment_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    users_service = UsersService(pg_pool=pg_pool)
    questions_service = QuestionsService(pg_pool=pg_pool)

    tg_user: TGUser = update.effective_user
    user: User = await users_service.get_or_create(tg_user=tg_user)

    await users_service.set_paid_status(user_id=user.id)
    await send_message(
        message=update.message, text=THANK_YOU_FOR_PAYMENT_TEXT, image=ImageType.thank_you
    )
    logger.info('User %d paid', user.id)

    # send question if possible
    new_question = await questions_service.get_new_random_question_for_user(user_id=user.id, user_level=user.level)
    if new_question:
        await send_question(
            message=update.message,
            question=new_question,
            questions_service=questions_service,
            user_id=user.id
        )

    return States.daily_question
