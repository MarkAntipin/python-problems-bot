from datetime import UTC, datetime

import asyncpg

from src.mappers.users import map_user_from_pg_row
from src.models.payment_status import PaymentStatus
from src.models.users import TelegramUser, User
from src.repositories.postgres.users import UsersRepo


class UsersService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.users_repo = UsersRepo(pg_pool=pg_pool)

    async def get_by_id(self, user_id: int) -> User:
        row = await self.users_repo.get_by_id(user_id=user_id)
        return map_user_from_pg_row(row=row)

    async def get_all(self) -> list[User]:
        rows = await self.users_repo.get_all()
        return [map_user_from_pg_row(row=row) for row in rows]

    async def get_or_create(self, tg_user: TelegramUser, came_from: str | None = None) -> User:
        row = await self.users_repo.create_or_update(
            telegram_id=tg_user.id,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            username=tg_user.username,
            language_code=tg_user.language_code,
            came_from=came_from
        )
        return map_user_from_pg_row(row=row)

    async def set_paid_status(self, user_id: int) -> None:
        now = datetime.utcnow()
        await self.users_repo.update(
            user_id=user_id,
            payment_status=PaymentStatus.paid,
            last_paid_at=now
        )

    async def set_trial_status(self, user_id: int) -> User:
        now = datetime.now(UTC)
        row = await self.users_repo.update(
            user_id=user_id,
            payment_status=PaymentStatus.trial,
            start_trial_at=now
        )
        return map_user_from_pg_row(row=row)

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

    async def set_status(self, user_id: int, status: str) -> None:
        await self.users_repo.update(
            user_id=user_id,
            status=status
        )
