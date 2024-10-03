import asyncpg
from telegram import User as TGUser

from src.models.users import TelegramUser, User


def map_user_from_pg_row(row: asyncpg.Record) -> User:
    return User.model_validate(dict(row))


def map_inner_telegram_user_from_tg_user(tg_user: TGUser) -> TelegramUser:
    return TelegramUser(
        id=tg_user.id,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name,
        username=tg_user.username,
        language_code=tg_user.language_code
    )
