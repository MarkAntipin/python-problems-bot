import asyncpg
from datetime import datetime, timedelta
from pytest_mock import MockerFixture
from src.tasks.send_advices import send_advices_task
from tests_functional.utils import add_advice, add_question, add_user, add_users_questions, add_users_send_advices
from src.services.advices import AdvicesService
from src.repositories.postgres.advices import AdvicesRepo


async def test_send_advices_task(pg: asyncpg.Pool, mocker: MockerFixture) -> None:
    mocker.patch('src.tasks.send_advices.Application', mocker.MagicMock())
    send_message_mock = mocker.patch('src.utils.telegram.send_message._send_message', return_value=True)

    await add_advice(pg=pg, level=1)
    advice_id_2 = await add_advice(pg=pg, level=2)

    question_id_1 = await add_question(pg=pg)
    question_id_2 = await add_question(pg=pg, theme='syntax')
    question_id_3 = await add_question(pg=pg)
    question_id_4 = await add_question(pg=pg)

    user_id_1 = await add_user(pg=pg, username='user_1')
    user_id_2 = await add_user(pg=pg, username='user_2')
    user_id_3 = await add_user(pg=pg, username='user_3')
    user_id_4 = await add_user(pg=pg, username='user_4')

    created_at_3 = datetime.utcnow() - timedelta(days=3)
    created_at_4 = datetime.utcnow() - timedelta(days=31)

    await add_users_questions(pg=pg, question_id=question_id_1, user_id=user_id_1, is_correct=False)
    await add_users_questions(pg=pg, question_id=question_id_2, user_id=user_id_2, is_correct=False)
    await add_users_questions(pg=pg, question_id=question_id_3, user_id=user_id_3, is_correct=False)
    await add_users_questions(pg=pg, question_id=question_id_4, user_id=user_id_4, is_correct=False)

    await add_users_send_advices(pg=pg, user_id=user_id_3, advice_id=advice_id_2, created_at=created_at_3)
    await add_users_send_advices(pg=pg, user_id=user_id_4, advice_id=advice_id_2, created_at=created_at_4)

    await send_advices_task(pg_pool=pg)

    row = await pg.fetchrow("""SELECT * FROM users_send_advices WHERE user_id = $1""", user_id_1)
    assert (
        row is not None
    )

    row = await pg.fetchrow("""SELECT * FROM users_send_advices WHERE user_id = $1""", user_id_2)
    assert (
        row is None
    )

    row = await pg.fetchrow("""SELECT COUNT(*) FROM users_send_advices WHERE user_id = $1""", user_id_3)
    assert (
        row['count'] == 1
    )

    row = await pg.fetchrow("""SELECT COUNT(*) FROM users_send_advices WHERE user_id = $1""", user_id_4)
    assert (
        row['count'] == 2
    )

    assert send_message_mock.call_count == 2


async def test_send_advice_task__short_time__not_send_advice(pg: asyncpg.Pool, mocker: MockerFixture) -> None:
    # arrange
    mocker.patch('src.tasks.send_advices.Application', mocker.MagicMock())
    send_message_mock = mocker.patch('src.utils.telegram.send_message._send_message', return_value=True)

    advice_id_1 = await add_advice(pg=pg, level=1)
    user_id_1 = await add_user(pg=pg, username='user_1')
    created_at_1 = datetime.utcnow() - timedelta(days=15)  # days < 30
    await add_users_send_advices(pg=pg, user_id=user_id_1, advice_id=advice_id_1, created_at=created_at_1)

    #act
    await send_advices_task(pg_pool=pg)

    # assert
    row = await pg.fetchrow("""SELECT * FROM users_send_advices WHERE user_id = $1""", user_id_1)
    assert (row is None)
    assert send_message_mock.call_count == 1


async def test_send_advice_task__no_weak_theme(pg: asyncpg.Pool, mocker: MockerFixture) -> None:
    # arrange
    mocker.patch('src.tasks.send_advices.Application', mocker.MagicMock())
    send_message_mock = mocker.patch('src.utils.telegram.send_message._send_message', return_value=True)

    user_id_2 = await add_user(pg=pg, username='user_2')

    #act
    row = await AdvicesRepo.get_weak_theme(user_id=user_id_2, user_level=2)

    #assert
    assert (row is None)
    assert send_message_mock.call_count == 1


async def test_send_advice_task__no_weak_theme__not_send(pg: asyncpg.Pool, mocker: MockerFixture) -> None:
    # arrange
    mocker.patch('src.tasks.send_advices.Application', mocker.MagicMock())
    send_message_mock = mocker.patch('src.utils.telegram.send_message._send_message', return_value=True)

    advice_id_3 = await add_advice(pg=pg, level=2)
    user_id_3 = await add_user(pg=pg, username='user_3')
    created_at_3 = datetime.utcnow() - timedelta(days=31)
    weak_theme = None

    await AdvicesRepo.get_send_advice(user_id=user_id_3, theme=weak_theme, level=2)
    await AdvicesService.get_new_advice_for_user(user_id=user_id_3, user_level=2)
    await add_users_send_advices(pg=pg, user_id=user_id_3, advice_id=advice_id_3, created_at=created_at_3)

    #act
    await send_advices_task(pg_pool=pg)

    #assert
    row = await pg.fetchrow("""SELECT * FROM users_send_advices WHERE user_id = $1""", user_id_3)
    assert (row is None)
    assert send_message_mock.call_count == 1


async def test_send_advice_task__long_time__send_advice(pg: asyncpg.Pool, mocker: MockerFixture) -> None:
    # arrange
    mocker.patch('src.tasks.send_advices.Application', mocker.MagicMock())
    send_message_mock = mocker.patch('src.utils.telegram.send_message._send_message', return_value=True)

    advice_id_4 = await add_advice(pg=pg, level=1)
    user_id_4 = await add_user(pg=pg, username='user_4')
    created_at_4 = datetime.utcnow() - timedelta(days=31)  # days >= 30
    await add_users_send_advices(pg=pg, user_id=user_id_4, advice_id=advice_id_4, created_at=created_at_4)

    #act
    await send_advices_task(pg_pool=pg)

    # assert
    row = await pg.fetchrow("""SELECT * FROM users_send_advices WHERE user_id = $1""", user_id_4)
    assert (row is not None)
    assert send_message_mock.call_count == 1
