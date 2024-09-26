from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_questions_service, get_users_service
from src.models.questions import AnswerRequest, AnswerResponse
from src.models.users import UserInitDataRaw
from src.services.questions import GetNewRandomQuestionForUserResp, QuestionsService
from src.services.users import UsersService

router = APIRouter(prefix='/api/v1/questions', tags=['questions'])


@router.post('/get-new-question', response_model=GetNewRandomQuestionForUserResp)
async def get_new_random_question_for_user(
    payload: UserInitDataRaw,
    users_service: UsersService = Depends(get_users_service),
    question_service: QuestionsService = Depends(get_questions_service)
) -> GetNewRandomQuestionForUserResp:
    user = await users_service.get_user_by_user_init_data(user_init_data_raw=payload.user_init_data)
    new_random_question = await question_service.get_new_random_question_for_user(
        user_id=user.id,
        user_level=user.level,
    )
    if not new_random_question.question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Not found question for user - {user.id}, level - {user.level}',
        )
    return new_random_question


@router.post('/answer', response_model=AnswerResponse)
async def answer_question(
    payload: AnswerRequest,
    users_service: UsersService = Depends(get_users_service),
    question_service: QuestionsService = Depends(get_questions_service)
) -> AnswerResponse:
    user = await users_service.get_user_by_user_init_data(user_init_data_raw=payload.user_init_data)
    question = await question_service.get_by_id(question_id=payload.question_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Not found question with id - {payload.question_id}'
        )
    is_correct = await question_service.answer_question(
        user_id=user.id,
        question=question,
        user_answer=payload.user_answer,
    )
    return AnswerResponse(is_correct=is_correct)
