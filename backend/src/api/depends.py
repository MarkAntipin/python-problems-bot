from fastapi import Request
from telegram import Bot

from src.services.achievements import AchievementsService
from src.services.questions import QuestionsService
from src.services.users import UsersService


async def get_questions_service(request: Request) -> QuestionsService:
    return QuestionsService(pg_pool=request.app.state.pg_pool)


async def get_users_service(request: Request) -> UsersService:
    return UsersService(pg_pool=request.app.state.pg_pool)


async def get_achievements_service(request: Request) -> AchievementsService:
    return AchievementsService(pg_pool=request.app.state.pg_pool)


def get_bot_instance(request: Request) -> Bot:
    return request.app.state.bot
