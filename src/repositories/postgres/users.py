import asyncpg


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
                    level
                FROM
                    users
                WHERE
                    id = $1
                """,
                user_id
            )
        return row

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
                    level
                FROM
                    users
                WHERE
                    telegram_id = $1
                """,
                telegram_id
            )
        return row

    async def create(
        self,
        telegram_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        username: str | None = None,
        language_code: str | None = None,
    ) -> asyncpg.Record:
        async with self.pg_pool.acquire() as conn:
            user_id = await conn.fetchrow(
                """
                INSERT INTO
                    users (
                        telegram_id,
                        first_name,
                        last_name,
                        username,
                        language_code
                    )
                VALUES (
                    $1,
                    $2,
                    $3,
                    $4,
                    $5
                )
                RETURNING
                    id,
                    level
                """,
                telegram_id,
                first_name,
                last_name,
                username,
                language_code
            )
        return user_id

    async def update_or_create(
        self,
        telegram_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        username: str | None = None,
        language_code: str | None = None,
    ) -> int:
        async with self.pg_pool.acquire() as conn:
            user_id = await conn.fetchrow(
                """
                INSERT INTO
                    users (
                        telegram_id,
                        first_name,
                        last_name,
                        username,
                        language_code
                    )
                VALUES (
                    $1,
                    $2,
                    $3,
                    $4,
                    $5
                ) ON CONFLICT (telegram_id) DO UPDATE
                SET
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    username = EXCLUDED.username,
                    language_code = EXCLUDED.language_code
                RETURNING id
                """,
                telegram_id,
                first_name,
                last_name,
                username,
                language_code
            )
        return user_id

    async def set_level(self, user_id: int, level: int) -> None:
        async with self.pg_pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE
                    users
                SET
                    level = $1
                WHERE
                    id = $2
                """,
                level,
                user_id
            )
