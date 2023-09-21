import asyncpg
from telegram import User as TGUser


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
                    language_code
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
                    language_code
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
        came_from: str | None = None
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
                        language_code,
                        came_from
                    )
                VALUES (
                    $1,
                    $2,
                    $3,
                    $4,
                    $5,
                    $6
                )
                RETURNING
                    id
                """,
                telegram_id,
                first_name,
                last_name,
                username,
                language_code,
                came_from
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

    async def get_top_users(self, limit: int = 3) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            query = f"""
            SELECT
                u.id,
                u.telegram_id,
                u.first_name,
                u.last_name,
                u.username,
                u.language_code,
                SUM(CASE WHEN uq.is_correct THEN 1 ELSE 0 END) as score
            FROM
                users AS u
            LEFT JOIN
                users_questions AS uq
            ON
                u.id = uq.user_id
            GROUP BY
                u.id,
                u.telegram_id,
                u.first_name,
                u.last_name,
                u.username,
                u.language_code
            ORDER BY
                score DESC
            LIMIT {limit}
            """
            rows = await conn.fetch(query)

        return rows

    async def get_user_position(self, tg_user: TGUser) -> int:
        async with self.pg_pool.acquire() as conn:
            query = """
            SELECT
                COUNT(*) + 1
            FROM (
                SELECT
                    u.id
                FROM
                    users AS u
                LEFT JOIN
                    users_questions AS uq
                ON
                    u.id = uq.user_id
                WHERE
                    uq.is_correct = TRUE
                GROUP BY
                    u.id
                HAVING
                    SUM(CASE WHEN uq.is_correct THEN 1 ELSE 0 END) > (
                        SELECT
                            SUM(CASE WHEN uq.is_correct THEN 1 ELSE 0 END)
                        FROM
                            users AS u
                        LEFT JOIN
                            users_questions AS uq
                        ON
                            u.id = uq.user_id
                        WHERE
                            u.telegram_id = $1
                    )
            ) AS leaders
            """
            position = await conn.fetchval(query, tg_user.id)

        return position

    async def get_user_score(self, tg_user: TGUser) -> int:
        async with self.pg_pool.acquire() as conn:
            query = """
            SELECT
                COALESCE(SUM(CASE WHEN uq.is_correct THEN 1 ELSE 0 END), 0) as score
            FROM
                users AS u
            LEFT JOIN
                users_questions AS uq
            ON
                u.id = uq.user_id
            WHERE
                u.telegram_id = $1
            """
            score = await conn.fetchval(query, tg_user.id)

        return score
