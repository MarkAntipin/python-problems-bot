import asyncpg
from pydantic import BaseModel

from src.repositories.postgres.leaders import LeadersRepo


class Leader(BaseModel):
    id: int  # noqa A003
    first_name: str
    username: str
    score: int


class LeadersService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.leaders_repo = LeadersRepo(pg_pool=pg_pool)

    async def get_top_users(self, limit: int) -> list[Leader] | None:
        top_users = await self.leaders_repo.get_top_users(limit=limit)
        if not top_users:
            return

        leaders = []
        for row in top_users:
            leader = Leader(
                id=row['id'],
                first_name=row['first_name'],
                username=row['username'],
                score=row['score'],
            )
            leaders.append(leader)
        return leaders

    async def get_user_position_and_score(self, user_id: int) -> dict:
        user_position_and_score = await self.leaders_repo.get_user_position_and_score(user_id)
        return user_position_and_score
