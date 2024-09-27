from datetime import datetime

from pydantic import BaseModel

from src.models.payment_status import PaymentStatus


class TelegramUser(BaseModel):
    id: int  # noqa A003
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None


class UserInitData(BaseModel):
    user: TelegramUser | None = None
    hash: str  # noqa A003


class UserInitDataRaw(BaseModel):
    """payload from telegram web app which need to be parsed into UserInitData"""
    user_init_data: str


class User(BaseModel):
    id: int  # noqa A003
    telegram_id: int
    payment_status: PaymentStatus
    level: int
    status: str
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    start_trial_at: datetime | None = None
    last_paid_at: datetime | None = None
    send_payment_at: datetime | None = None


class SetUserLevelRequest(UserInitDataRaw):
    level: int
