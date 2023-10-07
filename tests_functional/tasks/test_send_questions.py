from datetime import UTC, datetime, timedelta

import asyncpg
from pytest_mock import MockerFixture

from tasks.send_questions import send_daily_questions_task
from tests_functional.utils import add_question, add_user


async def test_send_daily_questions_task(
    pg: asyncpg.Pool,
    mocker: MockerFixture
) -> None:
    # arrange
    mocker.patch('tasks.send_questions.Application', mocker.MagicMock())
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


async def test_send_daily_questions_task__user_end_trial(
    pg: asyncpg.Pool,
    mocker: MockerFixture,
) -> None:
    # arrange
    mocker.patch('tasks.send_questions.Application', mocker.MagicMock())
    send_payment_mock = mocker.patch('tasks.send_questions.send_payment', return_value=True)

    await add_question(pg=pg)
    user_id = await add_user(
        pg=pg,
        start_trial_at=datetime.now(UTC) - timedelta(days=3),
        payment_status='trial'
    )

    # act
    await send_daily_questions_task(pg_pool=pg)

    # assert
    # check send payment
    assert send_payment_mock.call_count == 1

    # check user_have send_payment_at
    user = await pg.fetchrow("""SELECT * FROM users WHERE id = $1""", user_id)
    assert user['send_payment_at']

    # check questions is not send
    assert not (
        await pg.fetchrow("""SELECT * FROM users_send_questions WHERE user_id = $1""", user_id)
    )


async def test_send_daily_questions_task__user_end_trial__already_send_payment(
    pg: asyncpg.Pool,
    mocker: MockerFixture,
) -> None:
    # arrange
    mocker.patch('tasks.send_questions.Application', mocker.MagicMock())
    send_payment_mock = mocker.patch('tasks.send_questions.send_payment', return_value=True)

    await add_question(pg=pg)
    user_id = await add_user(
        pg=pg,
        start_trial_at=datetime.now(UTC) - timedelta(days=3),
        payment_status='trial',
        send_payment_at=datetime.now(UTC)
    )

    # act
    await send_daily_questions_task(pg_pool=pg)

    # assert
    # check payment is not send
    assert send_payment_mock.call_count == 0

    # check questions is not send
    assert not (
        await pg.fetchrow("""SELECT * FROM users_send_questions WHERE user_id = $1""", user_id)
    )
