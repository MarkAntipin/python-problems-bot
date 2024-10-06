from fastapi import APIRouter, Depends, HTTPException, Response, status
from telegram import Bot

from src.api.depends import get_bot_instance, get_users_service
from src.models.users import UserInitDataRaw
from src.services.users import UsersService
from src.utils.telegram.send_message import send_payment

router = APIRouter(prefix='/api/v1/payment', tags=['payment'])


@router.post('/send-payment')
async def send_payment_handler(
    payload: UserInitDataRaw,
    users_service: UsersService = Depends(get_users_service),
    bot: Bot = Depends(get_bot_instance)
) -> Response:
    user = await users_service.get_user_by_user_init_data(user_init_data_raw=payload.user_init_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid user_init_data')

    await send_payment(telegram_user_id=user.telegram_id, bot=bot)
    return Response(status_code=status.HTTP_200_OK)
