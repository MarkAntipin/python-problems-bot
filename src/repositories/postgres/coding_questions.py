import asyncpg


class CodingQuestionsRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def get_coding_question(self, coding_question_id: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT
                  title,
                  text,
                  def_init,
                  test_cases
                FROM
                  coding_questions
                WHERE
                  id = $1
                """,
                coding_question_id
            )

        return row
