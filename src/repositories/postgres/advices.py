from datetime import datetime

import asyncpg


# done
class AdvicesRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def get_month_sent_advices_count(self, user_id: int) -> int:
        month = datetime.utcnow().month

        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                  COUNT(*)
                FROM
                  users_send_advices
                WHERE
                  user_id = $1
                AND
                  created_at::date_month = $2
                """,
                user_id,
                month
            )

        return row['count']

    async def get_weak_theme(self, user_id: int, user_level: int) -> str:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                  count(is_correct) AS false_answers,
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

        return row['theme']

    async def get_advice_by_theme_and_level(self, theme: str, level: int) -> asyncpg.Record | None:
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

    async def get_by_id(self, advice_id: int) -> asyncpg.Record | None:
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

    async def user_feedback(self, user_id: int, advice_id: int, user_feedback: int | None, is_useful: bool) -> None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO
                  users_advices (
                    user_id,
                    advice_id,
                    user_feedback,
                    is_useful
                  )
                VALUES (
                  $1,
                  $2,
                  $3,
                  $4
                )
                """,
                user_id,
                advice_id,
                user_feedback,
                is_useful
            )

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
