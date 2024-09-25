from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_questions_service
from src.services.questions import QuestionsService

router = APIRouter(prefix='/api/v1/questions', tags=['questions'])


@router.get('/{question_id}')
async def get_question_by_id(
    question_id: int,
    questions_service: QuestionsService = Depends(get_questions_service)
) -> str:
    question = await questions_service.get_by_id(question_id=question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return question.text
