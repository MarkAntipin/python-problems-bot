import asyncpg
from telegram import User as TGUser


class LeadersRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def get_top_users(self, limit: int) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            query = """
            SELECT
                u.id,
                u.first_name,
                u.username,
                SUM(CASE WHEN uq.is_correct THEN 1 ELSE 0 END) as score
            FROM
                users AS u
            LEFT JOIN
                users_questions AS uq
            ON
                u.id = uq.user_id
            GROUP BY
                u.id,
                u.first_name,
                u.username
            ORDER BY
                score DESC
            LIMIT $1
            """
            rows = await conn.fetch(query, limit)

        return rows

    async def get_user_position_and_score(self, user_id: int) -> int:
        async with self.pg_pool.acquire() as conn:
            query = """
            select * from (
                SELECT
                    u.telegram_id as user_id,
                    COUNT(uq.is_correct) AS score,
                    row_number() OVER (ORDER BY COUNT(uq.is_correct) DESC) AS position
                FROM
                    users AS u
                LEFT JOIN
                    users_questions uq ON u.id = uq.user_id AND uq.is_correct = true
                GROUP BY
                    u.id
            ) leadersboard
                WHERE leadersboard.user_id = $1;
            """
            row = await conn.fetchrow(query, user_id)

        return {'position': row['position'], 'score': row['score']}
