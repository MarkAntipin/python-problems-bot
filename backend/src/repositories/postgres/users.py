from datetime import datetime

import asyncpg

from src.models.payment_status import PaymentStatus


class UsersRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def get_by_id(self, user_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    id,
                    telegram_id,
                    first_name,
                    last_name,
                    username,
                    language_code,
                    payment_status,
                    start_trial_at,
                    last_paid_at,
                    send_payment_at,
                    level,
                    status
                FROM
                    users
                WHERE
                    id = $1
                """,
                user_id
            )
        return row

    async def get_all(self) -> list[asyncpg.Record]:
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT
                    id,
                    telegram_id,
                    first_name,
                    last_name,
                    username,
                    language_code,
                    payment_status,
                    start_trial_at,
                    last_paid_at,
                    send_payment_at,
                    level,
                    status
                FROM
                    users
                """,
            )
        return rows

    async def get_by_telegram_id(self, telegram_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    id,
                    telegram_id,
                    first_name,
                    last_name,
                    username,
                    language_code,
                    payment_status,
                    start_trial_at,
                    last_paid_at,
                    send_payment_at,
                    level,
                    status
                FROM
                    users
                WHERE
                    telegram_id = $1
                """,
                telegram_id
            )
        return row

    async def create_or_update(
        self,
        telegram_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        username: str | None = None,
        language_code: str | None = None,
        came_from: str | None = None
    ) -> asyncpg.Record:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO
                    users (
                        telegram_id,
                        first_name,
                        last_name,
                        username,
                        language_code,
                        came_from,
                        payment_status
                    )
                VALUES (
                    $1,
                    $2,
                    $3,
                    $4,
                    $5,
                    $6,
                    $7
                )
                ON CONFLICT (telegram_id)
                DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    username = EXCLUDED.username,
                    language_code = EXCLUDED.language_code
                RETURNING
                    id,
                    telegram_id,
                    first_name,
                    last_name,
                    username,
                    language_code,
                    payment_status,
                    start_trial_at,
                    last_paid_at,
                    send_payment_at,
                    level,
                    status,
                    (xmax = 0) AS is_created
                """,
                telegram_id,
                first_name,
                last_name,
                username,
                language_code,
                came_from,
                PaymentStatus.onboarding.value
            )
        return row

    async def update(
        self,
        user_id: int,
        level: int | None = None,
        email: str | None = None,
        payment_status: PaymentStatus | None = None,
        start_trial_at: datetime | None = None,
        last_paid_at: datetime | None = None,
        send_payment_at: datetime | None = None,
        status: str = None,
    ) -> asyncpg.Record:
        _kwargs = {
            'payment_status': payment_status,
            'start_trial_at': start_trial_at,
            'last_paid_at': last_paid_at,
            'send_payment_at': send_payment_at,
            'level': level,
            'email': email,
            'status': status,
        }

        update_query = ''
        values = []
        for field, value in _kwargs.items():
            if value is not None:
                update_query += f'{field} = ${len(values) + 2}, '
                values.append(value)
        update_query = update_query.strip(', ')

        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                f"""
                UPDATE
                    users
                SET
                   {update_query}
                WHERE
                    id = $1
                RETURNING
                    id,
                    telegram_id,
                    first_name,
                    last_name,
                    username,
                    language_code,
                    payment_status,
                    start_trial_at,
                    last_paid_at,
                    send_payment_at,
                    level,
                    status
                """,
                user_id,
                *values
            )
        return row
