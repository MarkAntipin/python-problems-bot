import asyncpg

from src.services.users import UsersService
from tests_functional.utils import add_user


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
