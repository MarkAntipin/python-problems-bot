from fastapi import APIRouter, Depends

from src.api.depends import get_users_service
from src.models.users import User, UserInitDataRaw
from src.services.users import UsersService

router = APIRouter(prefix='/api/v1/users', tags=['users'])


@router.post('/get-user')
async def get_user(
    payload: UserInitDataRaw,
    users_service: UsersService = Depends(get_users_service)
) -> User:
    return await users_service.get_user_by_user_init_data(user_init_data_raw=payload.user_init_data)
