import asyncpg


class CodingQuestionsRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def get_random_coding_question(self, difficulty: int) -> asyncpg.Record | None:
        if difficulty == 1:
            diff = 'Easy'
        elif difficulty == 2:
            diff = 'Hard'
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                  id
                FROM
                  coding_questions
                WHERE
                  difficulty = $1
                """,
                diff
            )

        return row

    async def get_coding_question_by_id(self, coding_question_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                  title,
                  problem,
                  params,
                  return_type,
                  difficulty
                FROM
                  coding_questions
                WHERE
                  id = $1
                """,
                coding_question_id
            )

        return row

    async def get_test_cases(self, coding_question_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetch(
                """
                SELECT
                  input,
                  output
                FROM
                  coding_questions_tests
                WHERE
                  coding_question_id = $1
                """,
                coding_question_id
            )

        return row

    async def get_decided_coding_question(self, coding_question_id: int, user_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                  is_correct
                FROM
                  users_coding_questions
                WHERE
                  coding_question_id = $1
                AND
                  user_id = $2
                """,
                coding_question_id,
                user_id
            )

        return row

    async def decide_coding_question(self, coding_question_id: int, user_id: int) -> None:
        async with self.pg_pool.acquire() as conn:
            # можно убрать is_correct, т.к. добавлять в базу будет только тогда когда все правильно
            # либо сохранять последнюю запущенную попытку (код) пользователя
            row = await conn.fetchrow(
                """
                INSERT INTO
                  users_coding_questions (
                    coding_question_id,
                    user_id,
                    is_correct
                  )
                VALUES (
                  $1,
                  $2,
                  $3
                )
                """,
                coding_question_id,
                user_id,
                True
            )

        return row
