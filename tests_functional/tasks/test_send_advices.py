import asyncpg
from pytest_mock import MockerFixture

from tasks.send_advices import send_advices_task
from tests_functional.utils import add_advice, add_user, add_users_questions, add_question


async def test_send_advices_task(
    pg: asyncpg.Pool,
    mocker: MockerFixture
) -> None:
    mocker.patch('tasks.send_advices.Application', mocker.MagicMock())
    send_message_mock = mocker.patch('src.utils.telegram.send_message._send_message', return_value=True)

    await add_advice(pg=pg, level=1)
    await add_advice(pg=pg, level=2)

    question_id_1 = await add_question(pg=pg)
    question_id_2 = await add_question(pg=pg, theme='syntax')

    user_id_1 = await add_user(pg=pg, username='user_1')
    user_id_2 = await add_user(pg=pg, username='user_2')

    await add_users_questions(pg=pg, question_id=question_id_1, user_id=user_id_1, is_correct=False)
    await add_users_questions(pg=pg, question_id=question_id_2, user_id=user_id_2, is_correct=False)

    await send_advices_task(pg_pool=pg)

    # check send advices
    assert (
        await pg.fetchrow("""SELECT * FROM users_send_advices WHERE user_id = $1""", user_id_1)
    )

    row = await pg.fetchrow("""SELECT * FROM users_send_advices WHERE user_id = $1""", user_id_2)
    assert (
        row is None
    )

    # send 2 messages
    assert send_message_mock.call_count == 1
