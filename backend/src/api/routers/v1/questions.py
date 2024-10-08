from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_achievements_service, get_questions_service, get_users_service
from src.models.payment_status import PaymentStatus
from src.models.questions import AnswerRequest, AnswerResponse, Question
from src.models.users import UserInitDataRaw
from src.services.achievements import Achievement, AchievementsService
from src.services.questions import GetNewRandomQuestionForUserStatus, QuestionsService
from src.services.users import UsersService
from src.utils.payment import PaymentInfo, get_payment_info

router = APIRouter(prefix='/api/v1/questions', tags=['questions'])


@router.post('/get-new-question', response_model=Question)
async def get_new_question_for_user_handler(
    payload: UserInitDataRaw,
    users_service: UsersService = Depends(get_users_service),
    question_service: QuestionsService = Depends(get_questions_service)
) -> Question:
    user = await users_service.get_user_by_user_init_data(user_init_data_raw=payload.user_init_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user_init_data')

    payment_info: PaymentInfo = get_payment_info(user=user)
    if not payment_info.is_passed_paywall:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail='User has not passed paywall'
        )

    new_question_resp = await question_service.get_new_ordered_question_for_user(
        user_id=user.id,
        user_level=user.level,
    )
    if not new_question_resp.status == GetNewRandomQuestionForUserStatus.ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Not found question for user - {user.id}, level - {user.level}',
        )
    return new_question_resp.question


@router.post('/answer', response_model=AnswerResponse)
async def answer_question_handler(
    payload: AnswerRequest,
    users_service: UsersService = Depends(get_users_service),
    question_service: QuestionsService = Depends(get_questions_service),
    achievements_service: AchievementsService = Depends(get_achievements_service)
) -> AnswerResponse:
    user = await users_service.get_user_by_user_init_data(user_init_data_raw=payload.user_init_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user_init_data')

    # set trial status if user is in onboarding (he is starting to answer questions)
    if user.payment_status == PaymentStatus.onboarding:
        user = await users_service.set_trial_status(user_id=user.id)

    question = await question_service.get_by_id(question_id=payload.question_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Not found question with id - {payload.question_id}',
        )

    is_correct = await question_service.answer_question(
        user_id=user.id,
        question=question,
        user_answer=payload.user_answer,
    )

    achievements: list[Achievement] | None = await achievements_service.check_for_new_achievements(
        user_id=user.id
    )
    return AnswerResponse(is_correct=is_correct, achievements=achievements)

