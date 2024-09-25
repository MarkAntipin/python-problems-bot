import asyncpg

from pydantic import BaseModel
from src.repositories.postgres.advices import AdvicesRepo


class Advice(BaseModel):
    advice_id: int
    theme: str
    level: int
    link: str


class GetNewAdviceForUserResp(BaseModel):
    advice: Advice | None = None


class AdvicesService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.repo = AdvicesRepo(pg_pool=pg_pool)

    async def get_new_advice_for_user(self, user_id: int, user_level: int) -> GetNewAdviceForUserResp | None:
        weak_theme = await self.repo.get_weak_theme(user_id=user_id, user_level=user_level)
        if not weak_theme:
            return

        advice_send = await self.repo.get_send_advice(user_id, weak_theme['theme'], user_level)
        if advice_send:
            return

        advice = await self.repo.get_new_advice(weak_theme['theme'], user_level)
        if not advice:
            return

        return GetNewAdviceForUserResp(
            advice=Advice(
                advice_id=advice['id'],
                theme=advice['theme'],
                level=advice['level'],
                link=advice['link']
            )
        )

    async def get_by_id(self, advice_id: int) -> Advice | None:
        row = await self.repo.get_advice_by_id(advice_id=advice_id)
        if not row:
            return
        return Advice(
            advice_id=row['id'],
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
