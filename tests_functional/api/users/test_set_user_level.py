import typing as tp

import asyncpg
from fastapi.testclient import TestClient

from tests_functional.utils import add_user


async def test_set_user_level__ok(client: TestClient, pg: asyncpg.Pool, user_init_data: tp.Callable[..., str]) -> None:
    # arrange
    tg_user_id = 1
    level = 2
    changed_level = 1
    user_id = await add_user(pg=pg, telegram_id=tg_user_id, level=level)
    user_init_data_raw = user_init_data(user_id=tg_user_id)

    # act
    resp = client.post(
        '/api/v1/users/set-level',
        json={
            'user_init_data': user_init_data_raw,
            'level': changed_level
        },
    )

    # assert
    assert resp.status_code == 200

    user = await pg.fetchrow("""SELECT * FROM users WHERE id = $1""", user_id)
    assert user['level'] == changed_level
