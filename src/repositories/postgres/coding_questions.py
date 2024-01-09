from datetime import datetime

import asyncpg


class CodingQuestionsRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def get_today_answered_coding_questions_count(self, user_id: int) -> int:
        today = datetime.utcnow()
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    COUNT(*)
                FROM
                    users_coding_questions
                WHERE
                    user_id = $1
                AND
                    created_at::date = $2
                """,
                user_id,
                today.date()
            )

        return row['count']

    async def get_by_id(self, coding_question_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                  title,
                  text,
                  def_init
                FROM
                  coding_questions
                WHERE
                  id = $1
                """,
                coding_question_id
            )

        return row
