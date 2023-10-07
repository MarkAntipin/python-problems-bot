from datetime import UTC, datetime

import asyncpg
from pydantic import BaseModel
from telegram import User as TGUser

from src.repositories.postgres.users import UsersRepo
from src.services.models.payment_status import PaymentStatus


class User(BaseModel):
    id: int  # noqa A003
    telegram_id: int
    payment_status: PaymentStatus
    level: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    start_trial_at: datetime | None = None
    last_paid_at: datetime | None = None
    send_payment_at: datetime | None = None

    @classmethod
    def from_row(cls: 'User', row: asyncpg.Record) -> 'User':
        return User(
            id=row['id'],
            telegram_id=row['telegram_id'],
            payment_status=row['payment_status'],
            level=row['level'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            username=row['username'],
            language_code=row['language_code'],
            start_trial_at=row['start_trial_at'],
            last_paid_at=row['last_paid_at'],
            send_payment_at=row['send_payment_at'],
        )


class UsersService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.users_repo = UsersRepo(pg_pool=pg_pool)

    async def get_by_id(self, user_id: int) -> User:
        row = await self.users_repo.get_by_id(user_id=user_id)
        return User.from_row(row=row)

    async def get_all(self) -> list[User]:
        rows = await self.users_repo.get_all()
        return [User.from_row(row=row) for row in rows]

    async def get_or_create(self, tg_user: TGUser, came_from: str | None = None) -> User:
        row = await self.users_repo.get_by_telegram_id(telegram_id=tg_user.id)
        if not row:
            row = await self.users_repo.create(
                telegram_id=tg_user.id,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                username=tg_user.username,
                language_code=tg_user.language_code,
                came_from=came_from
            )
        return User.from_row(row=row)

    async def set_paid_status(self, user_id: int) -> None:
        now = datetime.now(UTC)
        await self.users_repo.update(
            user_id=user_id,
            payment_status=PaymentStatus.paid,
            last_paid_at=now
        )

    async def set_trial_status(self, user_id: int) -> None:
        now = datetime.now(UTC)
        await self.users_repo.update(
            user_id=user_id,
            payment_status=PaymentStatus.trial,
            start_trial_at=now
        )

    async def set_send_payment_at(self, user_id: int) -> None:
        now = datetime.now(UTC)
        await self.users_repo.update(
            user_id=user_id,
            send_payment_at=now
        )

    async def set_level(self, user_id: int, level: int) -> None:
        await self.users_repo.update(
            user_id=user_id,
            level=level
        )

    async def set_email(self, user_id: int, email: str) -> None:
        await self.users_repo.update(
            user_id=user_id,
            email=email
        )
