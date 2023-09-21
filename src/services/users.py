import asyncpg
from pydantic import BaseModel
from telegram import User as TGUser

from src.repositories.postgres.users import UsersRepo


class User(BaseModel):
    id: int  # noqa A003
    telegram_id: int
    first_name: str | None
    last_name: str | None
    username: str | None
    language_code: str | None


class UsersService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.users_repo = UsersRepo(pg_pool=pg_pool)
        self.pg_pool = pg_pool

    async def get_by_id(self, user_id: int) -> User:
        row = await self.users_repo.get_by_id(user_id=user_id)
        return User(
            id=row['id'],
            telegram_id=row['telegram_id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            username=row['username'],
            language_code=row['language_code']
        )

    async def get_or_create(self, tg_user: TGUser, came_from: str | None = None) -> User:
        row = await self.users_repo.get_by_telegram_id(telegram_id=tg_user.id)
        if not row:
            row = await self.users_repo.create(
                telegram_id=tg_user.id,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                username=tg_user.username,
                language_code=tg_user.language_code,
                came_from=came_from
            )
        return User(
            id=row['id'],
            telegram_id=tg_user.id,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            username=tg_user.username,
            language_code=tg_user.language_code,
        )

    async def update_or_create(self, user: TGUser) -> int:
        user_id: int = await self.users_repo.update_or_create(
            telegram_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            language_code=user.language_code,
        )
        return user_id

    async def get_top_users(self, limit=3):
        async with self.pg_pool.acquire() as conn:
            query = f"""
            SELECT u.id, u.telegram_id, u.first_name, u.last_name, u.username, u.language_code,
                   SUM(CASE WHEN uq.is_correct THEN 1 ELSE 0 END) as score
            FROM users AS u
            LEFT JOIN users_questions AS uq ON u.id = uq.user_id
            GROUP BY u.id, u.telegram_id, u.first_name, u.last_name, u.username, u.language_code
            ORDER BY score DESC
            LIMIT {limit}
            """
            rows = await conn.fetch(query)

        return rows

    async def get_user_position(self, tg_user: TGUser) -> int:
        async with self.pg_pool.acquire() as conn:
            query = """
            SELECT COUNT(*) + 1
            FROM (
                SELECT u.id
                FROM users AS u
                LEFT JOIN users_questions AS uq ON u.id = uq.user_id
                WHERE uq.is_correct = TRUE
                GROUP BY u.id
                HAVING SUM(CASE WHEN uq.is_correct THEN 1 ELSE 0 END) > (
                    SELECT SUM(CASE WHEN uq.is_correct THEN 1 ELSE 0 END)
                    FROM users AS u
                    LEFT JOIN users_questions AS uq ON u.id = uq.user_id
                    WHERE u.telegram_id = $1
                )
            ) AS leaders
            """
            position = await conn.fetchval(query, tg_user.id)

        return position

    async def get_user_score(self, tg_user: TGUser) -> int:
        async with self.pg_pool.acquire() as conn:
            query = """
            SELECT COALESCE(SUM(CASE WHEN uq.is_correct THEN 1 ELSE 0 END), 0) as score
            FROM users AS u
            LEFT JOIN users_questions AS uq ON u.id = uq.user_id
            WHERE u.telegram_id = $1
            """
            score = await conn.fetchval(query, tg_user.id)

        return score
