import asyncpg
from pydantic import BaseModel

from src.repositories.postgres.advices import AdvicesRepo
from src.utils.is_advice_useful import is_advice_useful


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

    async def get_new_advice_for_user(self, user_id: int, user_level: int) -> GetNewAdviceForUserResp:
        weak_theme = await self.repo.get_weak_theme(
            user_id=user_id,
            user_level=user_level
        )
        row = await self.repo.get_advice_by_theme_and_level(weak_theme, user_level)
        #  берем тему, по которой у пользователя больше всего неправильных ответов
        #  делаю нерандомно как в вопросах, потому что если пользователь долгое время не отвечает правильно на эту тему,
        #  то мы должны отправлять советы именно по этой теме, а не по случайной

        return GetNewAdviceForUserResp(
            advice=Advice(
                id=row['id'],
                theme=row['theme'],
                level=row['level'],
                link=row['link']
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

    async def useful_advice(
        self,
        user_id: int,
        advice: Advice,
        user_feedback: int | None  # 0 or 1, no or yes; mb str
    ) -> bool:
        is_useful = is_advice_useful(user_feedback=user_feedback)
        await self.repo.user_feedback(
            advice_id=advice.id,
            user_id=user_id,
            user_feedback=user_feedback,
            is_useful=is_useful,
        )
        return is_useful

    async def send_advice(
        self,
        user_id: int,
        advice_id: int
    ) -> None:
        await self.repo.send_advice(
            advice_id=advice_id,
            user_id=user_id,
        )
