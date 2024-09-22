from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_users_service
from src.models.users import User, UserInitData, UserInitDataRaw
from src.services.users import UsersService
from src.utils.user_init_data import validate_and_parce_user_init_data

router = APIRouter(prefix='/api/v1/users', tags=['users'])


@router.post('/get-user')
async def get_user(
    payload: UserInitDataRaw,
    users_service: UsersService = Depends(get_users_service)
) -> User:
    user_init_data: UserInitData = validate_and_parce_user_init_data(user_init_data_raw=payload.user_init_data)
    if not user_init_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user_init_data')

    user: User = await users_service.get_or_create(tg_user=user_init_data.user)
    return user
