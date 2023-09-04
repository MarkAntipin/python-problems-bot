import asyncpg


class OnboardingQuestionsRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def get_new_question_for_user(self, user_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    oq.id,
                    oq.text,
                    oq.answer,
                    oq.choices
                FROM
                    onboarding_questions oq
                LEFT JOIN
                    users_onboarding_questions ugq ON oq.id = ugq.onboarding_question_id
                AND
                    ugq.user_id = $1
                WHERE
                    ugq.answer IS NULL
                ORDER BY oq.order
                """,
                user_id
            )
        return row

    async def get_by_id(self, question_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                    id,
                    text,
                    answer,
                    choices
                FROM
                    onboarding_questions
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
                    users_onboarding_questions (
                        answer,
                        onboarding_question_id,
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

    async def get_user_answered_onboarding_questions(self, user_id: int) -> list[asyncpg.Record]:
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT DISTINCT ON (uoq.onboarding_question_id)
                    uoq.is_correct,
                    oq."level"
                FROM
                    users_onboarding_questions uoq
                JOIN
                    onboarding_questions oq ON uoq.onboarding_question_id = oq.id
                WHERE
                    uoq.user_id = $1;
                """,
                user_id
            )
        return rows

    async def send_question(
            self,
            user_id: int,
            question_id: int,
    ) -> None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                INSERT INTO
                    users_send_onboarding_questions (
                        onboarding_question_id,
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
