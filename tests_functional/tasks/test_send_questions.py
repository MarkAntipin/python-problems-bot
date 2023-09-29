import asyncpg

from tests_functional.utils import add_question, add_user
from tasks.send_questions import send_daily_questions_task


async def test_send_daily_questions_task(
    pg: asyncpg.Pool,
    mocker
) -> None:
    # arrange
    send_message_mock = mocker.patch('src.utils.telegram.send_message._send_message', return_value=True)

    await add_question(pg=pg)
    await add_question(pg=pg)
    user_id_1 = await add_user(pg=pg, username='user_1')
    user_id_2 = await add_user(pg=pg, username='user_2')

    # act
    await send_daily_questions_task(pg_pool=pg)

    # assert
    # check send questions
    assert (
        await pg.fetchrow("""SELECT * FROM users_send_questions WHERE user_id = $1""", user_id_1)
    )
    assert (
        await pg.fetchrow("""SELECT * FROM users_send_questions WHERE user_id = $1""", user_id_2)
    )

    # send 2 messages
    assert send_message_mock.call_count == 2