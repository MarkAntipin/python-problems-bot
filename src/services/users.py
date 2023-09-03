import asyncpg
from pydantic import BaseModel
from telegram import User as TGUser

from src.repositories.postgres.onboarding_questions import OnboardingQuestionsRepo
from src.repositories.postgres.users import UsersRepo
from src.utils.calculate_user_level import calculate_user_level


class User(BaseModel):
    id: int  # noqa A003
    telegram_id: int
    level: int | None
    first_name: str | None
    last_name: str | None
    username: str | None
    language_code: str | None


class UsersService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.users_repo = UsersRepo(pg_pool=pg_pool)
        self.onboarding_questions_repo = OnboardingQuestionsRepo(pg_pool=pg_pool)

    async def get_by_id(self, user_id: int) -> User:
        row = await self.users_repo.get_by_id(user_id=user_id)
        return User(
            id=row['id'],
            telegram_id=row['telegram_id'],
            level=row['level'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            username=row['username'],
            language_code=row['language_code']
        )

    async def get_or_create(self, tg_user: TGUser) -> User:
        row = await self.users_repo.get_by_telegram_id(telegram_id=tg_user.id)
        if not row:
            row = await self.users_repo.create(
                telegram_id=tg_user.id,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                username=tg_user.username,
                language_code=tg_user.language_code,
            )
        return User(
            id=row['id'],
            telegram_id=tg_user.id,
            level=row['level'],
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

    async def set_level(self, user_id: int) -> int:
        rows = await self.onboarding_questions_repo.get_user_answered_onboarding_questions(
            user_id=user_id
        )
        if not rows:
            user_level = 1
        else:
            user_level: int = calculate_user_level(
                all_answers_levels=[r['level'] for r in rows if r['level']],
                correct_answer_levels=[r['level'] for r in rows if r['level'] and r['is_correct'] is True]
            )
        await self.users_repo.set_level(user_id=user_id, level=user_level)
        return user_level
