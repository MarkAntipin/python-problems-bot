from fastapi import Request

from src.services.questions import QuestionsService


async def get_questions_service(request: Request) -> QuestionsService:
    return QuestionsService(pg_pool=request.app.state.pg_pool)
