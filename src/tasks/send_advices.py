import asyncio
import logging
import asyncpg

from telegram.ext import Application

from settings import bot_settings
from src.services.advices import AdvicesService
from src.services.users import User, UsersService
from src.utils.telegram.send_message import send_advice

logger = logging.getLogger(__name__)


async def send_advices_task(pg_pool: asyncpg.Pool) -> None:
    bot = Application.builder().token(bot_settings.TOKEN).build().bot

    users_service = UsersService(pg_pool=pg_pool)
    advices_service = AdvicesService(pg_pool=pg_pool)

    users: list[User] = await users_service.get_all()
    for user in users:
        if user.status != 'active':
            continue

        new_advice_resp = await advices_service.get_new_advice_for_user(
            user_id=user.id,
            user_level=user.level
        )

        if not new_advice_resp:
            continue

        is_sent = await send_advice(
            bot=bot,
            chat_id=user.telegram_id,
            advice=new_advice_resp.advice,
            advices_service=advices_service,
            user_id=user.id
        )

        if is_sent:
            logger.info('Advice sent to user %d', user.id)
        else:
            await users_service.set_status(user_id=user.id, status='block_bot')
            logger.info('User %d blocked bot', user.id)
        await asyncio.sleep(0.1)
