import asyncpg
from pydantic import BaseModel
from telegram import User as TGUser

from src.repositories.postgres.leaders import LeadersRepo


class Leader(BaseModel):
    id: int  # noqa A003
    first_name: str
    username: str
    score: int

class LeadersService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.leaders_repo = LeadersRepo(pg_pool=pg_pool)

    async def get_top_users(self, limit: int) -> list[TGUser]:
        leaders = await self.leaders_repo.get_top_users(limit=limit)
        users = []
        for row in leaders:
            user = Leader(
                id=row['id'],
                first_name=row['first_name'],
                username=row['username'],
                score=row['score'],
            )
            users.append(user)
        return users

    async def get_user_position_and_score(self, user_id: int) -> dict:
        return await self.leaders_repo.get_user_position_and_score(user_id)
