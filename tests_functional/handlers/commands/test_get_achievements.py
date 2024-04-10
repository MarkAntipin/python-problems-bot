import asyncpg
from pytest_mock import MockerFixture
from telegram import User as TGUser

from src.bot.handlers.commands import get_achievements_handler
from tests_functional.utils import add_user, add_user_achievement


async def test_get_achievements_handler(
    pg: asyncpg.Pool,
    mocker: MockerFixture
) -> None:
    # arrange
    telegram_id = 1
    user_id = await add_user(pg=pg, telegram_id=telegram_id, level=1)
    await add_user_achievement(pg=pg, user_id=user_id, achievement_name='first_correct_answer')

    update_mock = mocker.AsyncMock()
    update_mock.update.message.from_user = TGUser(id=telegram_id, is_bot=False, first_name='first_name')
    await mocker.patch('src.bot.handlers.commands.pg_pool', pg)

    # act
    await get_achievements_handler(update_mock, None)

    # assert
    # send message
    assert update_mock.message.reply_text.call_count == 1
    assert update_mock.message.reply_text.call_args.kwargs['text'] == (
        '*Твои достижения:*\n\n'
        'Первая правильно решенная задача \\- *Hello World\\!* 🚀\n\n'
        'Получено 1 из 17'
    )
