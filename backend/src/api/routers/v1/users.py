import logging

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_users_service
from src.models.users import SetUserLevelRequest, User, UserInitDataRaw
from src.services.users import UsersService

logger = logging.getLogger(__name__)


router = APIRouter(prefix='/api/v1/users', tags=['users'])


@router.post('/get-user')
async def get_user(
    payload: UserInitDataRaw,
    users_service: UsersService = Depends(get_users_service)
) -> User:
    user = await users_service.get_user_by_user_init_data(user_init_data_raw=payload.user_init_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user_init_data')

    logger.info(f'Found user with ID: {user.id}, level: {user.level}')

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

    logger.info(f'Set level: {user.level}, for user with ID {user.id}')

    return user
