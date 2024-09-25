from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_questions_service
from src.api.schemas.questions import AnswerRequest, AnswerResponse, IsAnsweredAllResponse
from src.services.questions import GetNewRandomQuestionForUserResp, Question, QuestionsService

router = APIRouter(prefix='/api/v1/questions', tags=['questions'])


@router.get('/{question_id}', response_model=Question)
async def get_question_by_id(
    question_id: int,
    questions_service: QuestionsService = Depends(get_questions_service)
) -> Question:
    question = await questions_service.get_by_id(question_id=question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return question


@router.get('/user/{user_id}/level/{user_level}', response_model=GetNewRandomQuestionForUserResp)
async def get_new_random_question_for_user(
    user_id: int,
    user_level: int,
    question_service: QuestionsService = Depends(get_questions_service)
) -> GetNewRandomQuestionForUserResp:
    new_random_question = await question_service.get_new_random_question_for_user(
        user_id=user_id,
        user_level=user_level,
    )
    if not new_random_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return new_random_question


@router.get('/user/{user_id}/answered-all', response_model=IsAnsweredAllResponse)
async def is_answered_all_questions_for_today(
    user_id: int,
    question_service: QuestionsService = Depends(get_questions_service)
) -> IsAnsweredAllResponse:
    is_answered_all = await question_service.is_answered_all_questions_for_today(user_id=user_id)
    return IsAnsweredAllResponse(is_answered_all=is_answered_all)


@router.post('/answer', response_model=AnswerResponse)
async def answer_question(
    answer_data: AnswerRequest,
    question_service: QuestionsService = Depends(get_questions_service)
) -> AnswerResponse:
    question = await question_service.get_by_id(question_id=answer_data.question_id)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    is_correct = await question_service.answer_question(
        user_id=answer_data.user_id,
        question=question,
        user_answer=answer_data.user_answer,
    )
    return AnswerResponse(is_correct=is_correct)
