import asyncpg
from settings import bot_settings


# done
class AdvicesRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def get_weak_theme(self, user_id: int, user_level: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                  count(*) AS false_answers,
                  theme
                FROM
                  users_questions t1
                  JOIN questions t2
                    ON t1.question_id = t2.id
                WHERE
                  is_correct = 'false'
                AND
                  user_id = $1
                AND
                  level = $2
                GROUP BY
                  user_id,
                  t2.id,
                  is_correct,
                  theme,
                  level
                ORDER BY
                  user_id,
                  false_answers DESC,
                  level
                LIMIT 1
                """,
                user_id,
                user_level,
            )

        return row

    async def get_new_advice(self, theme: str, level: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                  id,
                  theme,
                  level,
                  link
                FROM
                  advices
                WHERE
                  theme = $1
                AND
                  level = $2;
                """,
                theme,
                level,
            )

        return row

    async def get_advice_by_id(self, advice_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    id,
                    theme,
                    level,
                    link
                FROM
                    advices
                WHERE
                    id = $1
                """,
                advice_id
            )

        return row

    async def get_send_advice(self, user_id: int, theme: str, level: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                  id
                FROM
                  advices
                  JOIN users_send_advices
                    ON advices.id = users_send_advices.advice_id
                WHERE
                  user_id = $1
                AND
                  created_at BETWEEN CURRENT_DATE - $4 AND CURRENT_DATE
                AND
                  theme = $2
                AND
                  level = $3;
                """,
                user_id,
                theme,
                level,
                bot_settings.WEAK_THEMES_ADVICE_INTERVAL,
            )

        return row

    async def send_advice(self, user_id: int, advice_id: int) -> None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO
                  users_send_advices (
                        user_id,
                        advice_id
                  )
                VALUES (
                    $1,
                    $2
                )
                """,
                user_id,
                advice_id
            )

        return row
