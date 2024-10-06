from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_achievements_service, get_leaders_service, get_users_service
from src.models.users import SetUserLevelRequest, User, UserInitDataRaw, UserProfile
from src.services.achievements import AchievementsService
from src.services.leaders import LeadersService
from src.services.users import UsersService

router = APIRouter(prefix='/api/v1/users', tags=['users'])


@router.post('/get-user')
async def get_user(
    payload: UserInitDataRaw,
    users_service: UsersService = Depends(get_users_service)
) -> User:
    user = await users_service.get_user_by_user_init_data(user_init_data_raw=payload.user_init_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user_init_data')
    return user


@router.post('/set-level')
async def set_user_level(
    payload: SetUserLevelRequest,
    users_service: UsersService = Depends(get_users_service)
) -> User:
    user = await users_service.get_user_by_user_init_data(user_init_data_raw=payload.user_init_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user_init_data')

    await users_service.set_level(user_id=user.id, level=payload.level)

    return user


@router.post('/get-user-profile')
async def get_user_profile(
    payload: UserInitDataRaw,
    users_service: UsersService = Depends(get_users_service),
    achievements_service: AchievementsService = Depends(get_achievements_service),
    leaders_service: LeadersService = Depends(get_leaders_service)
) -> UserProfile:
    user = await users_service.get_user_by_user_init_data(user_init_data_raw=payload.user_init_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user_init_data')
    user_position_and_score = await leaders_service.get_user_in_leaders(user_id=user.id)
    achievements = await achievements_service.get_user_achievements(user_id=user.id)
    user_profile = UserProfile(
        username=user.username,
        user_position=user_position_and_score.position,
        achievements=achievements
    )
    return user_profile
