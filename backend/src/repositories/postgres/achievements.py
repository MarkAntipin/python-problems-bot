import asyncpg


class AchievementsRepo:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.pg_pool = pg_pool

    async def get_user_achievements_names(self, user_id: int) -> set[str]:
        async with self.pg_pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT
                    achievement_name
                FROM
                    users_achievements
                WHERE
                    user_id = $1
                """,
                user_id
            )
        return {row['achievement_name'] for row in rows}

    async def save_achievements(self, user_id: int, achievement_names: list[str]) -> asyncpg.Record | None:
        async with self.pg_pool.acquire() as conn:
            await conn.copy_records_to_table(
                'users_achievements',
                records=[(user_id, achievement_name) for achievement_name in achievement_names],
                columns=['user_id', 'achievement_name'],
            )
