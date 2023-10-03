from telegram import Update
from telegram import User as TGUser
from telegram.ext import (
    ContextTypes,
)

from bot.handlers.states import States
from src.services.users import User, UsersService
from src.utils.postgres_pool import pg_pool


async def pre_checkout_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query
    await query.answer(ok=True)


async def successful_payment_handler(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    users_service = UsersService(pg_pool=pg_pool)

    tg_user: TGUser = update.effective_user
    user: User = await users_service.get_or_create(tg_user=tg_user)
    await users_service.set_paid_status(user_id=user.id)

    # TODO: send throw send message; and add picture
    await update.message.reply_text('Спасибо больше за оплату!')
    return States.daily_question
