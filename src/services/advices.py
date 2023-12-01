import asyncpg
from pydantic import BaseModel

from src.repositories.postgres.advices import AdvicesRepo


class Advice(BaseModel):
    id: int
    theme: str
    level: int
    link: str


class GetNewAdviceForUserResp(BaseModel):
    advice: Advice | None = None


class AdvicesService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.repo = AdvicesRepo(pg_pool=pg_pool)

    async def get_new_advice_for_user(self, user_id: int, user_level: int) -> GetNewAdviceForUserResp | None:
        weak_theme = await self.repo.get_weak_theme(
            user_id=user_id,
            user_level=user_level
        )

        if not weak_theme:
            return

        advice = await self.repo.get_advice_by_theme_and_level(weak_theme['theme'], user_level)

        if not advice:
            return

        return GetNewAdviceForUserResp(
            advice=Advice(
                id=advice['id'],
                theme=advice['theme'],
                level=advice['level'],
                link=advice['link']
            )
        )

    async def get_by_id(self, advice_id: int) -> Advice | None:
        row = await self.repo.get_by_id(advice_id=advice_id)
        if not row:
            return
        return Advice(
                id=row['id'],
                theme=row['theme'],
                level=row['level'],
                link=row['link']
            )

    async def send_advice(
        self,
        user_id: int,
        advice_id: int
    ) -> None:
        await self.repo.send_advice(
            advice_id=advice_id,
            user_id=user_id,
        )
