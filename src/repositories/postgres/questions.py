from datetime import UTC, datetime

import asyncpg


class QuestionsRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def get_today_send_questions_count(self, user_id: int) -> int:
        today = datetime.now(UTC)
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    COUNT(*)
                FROM
                    users_send_questions
                WHERE
                    user_id = $1
                AND
                    created_at::date = $2
                """,
                user_id,
                today.date()
            )
        return row['count']

    async def get_new_questions_for_user(
            self, user_id: int, level: int, limit: int = 10
    ) -> list[asyncpg.Record]:
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT
                    q.id,
                    q.text,
                    q.answer,
                    q.explanation,
                    q.choices
                FROM
                    questions q
                LEFT JOIN
                    users_questions uq ON q.id = uq.question_id
                AND
                    uq.user_id = $1
                WHERE
                    uq.answer IS NULL
                AND
                    q.level = $2
                LIMIT
                    $3
                """,
                user_id,
                level,
                limit
            )
        return rows

    async def get_by_id(self, question_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    id,
                    text,
                    answer,
                    choices,
                    explanation
                FROM
                    questions
                WHERE
                    id = $1
                """,
                question_id
            )
        return row

    async def answer_question(
            self,
            user_id: int,
            question_id: int,
            user_answer: str,
            is_correct: bool
    ) -> None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO
                    users_questions (
                        answer,
                        question_id,
                        user_id,
                        is_correct
                    )
                VALUES (
                    $1,
                    $2,
                    $3,
                    $4
                )
                """,
                user_answer,
                question_id,
                user_id,
                is_correct
            )
        return row

    async def send_question(
            self,
            user_id: int,
            question_id: int,
    ) -> None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO
                    users_send_questions (
                        question_id,
                        user_id
                    )
                VALUES (
                    $1,
                    $2
                )
                """,
                question_id,
                user_id,
            )
        return row
