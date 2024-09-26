from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_questions_service, get_users_service
from src.api.routers.v1.users import get_user
from src.models.questions import AnswerRequest, AnswerResponse
from src.models.users import User, UserInitDataRaw
from src.services.questions import GetNewRandomQuestionForUserResp, QuestionsService
from src.services.users import UsersService

router = APIRouter(prefix='/api/v1/questions', tags=['questions'])


@router.post('/get-new-question', response_model=GetNewRandomQuestionForUserResp)
async def get_new_random_question_for_user(
    user: User = Depends(get_user),
    question_service: QuestionsService = Depends(get_questions_service)
) -> GetNewRandomQuestionForUserResp:
    new_random_question = await question_service.get_new_random_question_for_user(
        user_id=user.id,
        user_level=user.level,
    )
    if not new_random_question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Not found question for user - {user.id}, level - {user.level}',
        )
    return new_random_question


async def _get_user_from_answer_request(
    answer_data: AnswerRequest,
    users_service: UsersService = Depends(get_users_service),
) -> User:
    payload = UserInitDataRaw(user_init_data=answer_data.user_init_data)
    user = await get_user(payload=payload, users_service=users_service)
    return user


@router.post('/answer', response_model=AnswerResponse)
async def answer_question(
    answer_data: AnswerRequest,
    user: User = Depends(_get_user_from_answer_request),
    question_service: QuestionsService = Depends(get_questions_service)
) -> AnswerResponse:
    question = await question_service.get_by_id(question_id=answer_data.question_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Not found question with id - {answer_data.question_id}'
        )
    is_correct = await question_service.answer_question(
        user_id=user.id,
        question=question,
        user_answer=answer_data.user_answer,
    )
    return AnswerResponse(is_correct=is_correct)
