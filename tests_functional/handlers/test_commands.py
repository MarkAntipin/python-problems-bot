import asyncpg
from pytest_mock import MockerFixture
from telegram import User as TGUser

from bot.handlers.comands import set_difficult_handler, set_easy_handler
from tests_functional.utils import add_user


async def test_set_difficult_handler(
    pg: asyncpg.Pool,
    mocker: MockerFixture
) -> None:
    # arrange
    user_id = await add_user(pg=pg, telegram_id=1, level=1)

    update_mock = mocker.AsyncMock()
    update_mock.update.message.from_user = TGUser(id=1, is_bot=False, first_name='first_name')
    mocker.patch('bot.handlers.comands.pg_pool', pg)

    # act
    await set_difficult_handler(update_mock, None)

    # assert
    user = await pg.fetchrow("""SELECT * FROM users WHERE id = $1""", user_id)
    assert user['level'] == 2


async def test_set_easy_handler(
    pg: asyncpg.Pool,
    mocker: MockerFixture
) -> None:
    # arrange
    user_id = await add_user(pg=pg, telegram_id=1, level=2)

    update_mock = mocker.AsyncMock()
    update_mock.update.message.from_user = TGUser(id=1, is_bot=False, first_name='first_name')
    mocker.patch('bot.handlers.comands.pg_pool', pg)

    # act
    await set_easy_handler(update_mock, None)

    # assert
    user = await pg.fetchrow("""SELECT * FROM users WHERE id = $1""", user_id)
    assert user['level'] == 1
