from datetime import UTC, datetime, timedelta

import asyncpg
from pytest_mock import MockerFixture

from src.tasks.send_questions import send_daily_questions_task
from tests_functional.utils import add_question, add_user


async def test_send_daily_questions_task(
    pg: asyncpg.Pool,
    mocker: MockerFixture
) -> None:
    # arrange
    mocker.patch('src.tasks.send_questions.Application', mocker.MagicMock())
    send_message_mock = mocker.patch('src.utils.telegram.send_message._send_message', return_value=True)

    await add_question(pg=pg)
    await add_question(pg=pg)
    await add_user(pg=pg, username='user_1')
    await add_user(pg=pg, username='user_2')

    # act
    await send_daily_questions_task(pg_pool=pg)

    # assert
    # send 2 messages
    assert send_message_mock.call_count == 2


async def test_send_daily_questions_task__user_baned_bot(
    pg: asyncpg.Pool,
    mocker: MockerFixture
) -> None:
    # arrange
    mocker.patch('src.tasks.send_questions.Application', mocker.MagicMock())
    mocker.patch('src.utils.telegram.send_message._send_message', return_value=False)

    await add_question(pg=pg)
    await add_question(pg=pg)
    user_id_1 = await add_user(pg=pg, username='user_1')

    # act
    await send_daily_questions_task(pg_pool=pg)

    # assert
    # check user set as blocked
    user = (
        await pg.fetchrow("""SELECT * FROM users WHERE id = $1""", user_id_1)
    )
    assert user['status'] == 'block_bot'


async def test_send_daily_questions_task__user_not_payed(
    pg: asyncpg.Pool,
    mocker: MockerFixture,
) -> None:
    # arrange
    mocker.patch('src.tasks.send_questions.Application', mocker.MagicMock())
    mocker.patch('src.tasks.send_questions.bot_settings.ENABLE_PAYMENT', True)
    send_payment_mock = mocker.patch('src.tasks.send_questions.send_payment', return_value=True)
    user_id_1 = await add_user(
        pg=pg, username='user_1', payment_status='trial', start_trial_at=datetime.now(UTC) - timedelta(days=4)
    )
    await add_question(pg=pg)

    # act
    await send_daily_questions_task(pg_pool=pg)

    # assert
    user = (
        await pg.fetchrow("""SELECT * FROM users WHERE id = $1""", user_id_1)
    )

    # send 1 message with payment
    assert user['send_payment_at'] is not None
    assert send_payment_mock.call_count == 1


async def test_send_daily_questions_task__user_not_payed__already_send_payment(
    pg: asyncpg.Pool,
    mocker: MockerFixture
) -> None:
    # arrange
    mocker.patch('src.tasks.send_questions.Application', mocker.MagicMock())
    send_payment_mock = mocker.patch('src.tasks.send_questions.send_payment', return_value=True)
    await add_user(
        pg=pg,
        username='user_1',
        payment_status='trial',
        start_trial_at=datetime.now(UTC) - timedelta(days=4),
        send_payment_at=datetime.now(UTC)
    )

    # act
    await send_daily_questions_task(pg_pool=pg)

    # assert
    # payment already sent
    assert not send_payment_mock.call_count
