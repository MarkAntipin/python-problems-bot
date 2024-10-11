import asyncpg

from src.services.users import UsersService
from tests_functional.utils import add_question, add_user, add_users_questions


async def test_set_paid_status(
    pg: asyncpg.Pool,
) -> None:
    # arrange
    user_id = await add_user(pg=pg)

    # act
    service = UsersService(pg_pool=pg)
    await service.set_paid_status(user_id=user_id)

    # assert
    user = await pg.fetchrow("""SELECT * FROM users WHERE id = $1""", user_id)
    assert user['payment_status'] == 'paid'
    assert user['last_paid_at']


async def test_set_trial_status(
    pg: asyncpg.Pool,
) -> None:
    # arrange
    user_id = await add_user(pg=pg)

    # act
    service = UsersService(pg_pool=pg)
    await service.set_trial_status(user_id=user_id)

    # assert
    user = await pg.fetchrow("""SELECT * FROM users WHERE id = $1""", user_id)
    assert user['payment_status'] == 'trial'
    assert user['start_trial_at']


async def test_get_info(
        pg: asyncpg.Pool,
) -> None:
    # arrange
    user_id_1 = await add_user(pg=pg, username='user_1')
    question_id_1 = await add_question(pg=pg)
    question_id_2 = await add_question(pg=pg)
    await add_users_questions(pg=pg, question_id=question_id_1, user_id=user_id_1, is_correct=True)
    await add_users_questions(pg=pg, question_id=question_id_2, user_id=user_id_1, is_correct=False)

    # act
    service = UsersService(pg_pool=pg)
    result = await service.get_info(user_id=user_id_1)

    # assert
    assert len(result) == 1
    assert result['total_questions_answered'] == 2
    assert result['correct_answers_percentage'] == 50
