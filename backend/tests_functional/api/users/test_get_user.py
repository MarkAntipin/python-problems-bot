import typing as tp

import asyncpg
from fastapi.testclient import TestClient

from tests_functional.utils import add_user


async def test_get_user__ok(client: TestClient, pg: asyncpg.Pool, user_init_data: tp.Callable[..., str]) -> None:
    # arrange
    tg_user_id = 1
    level = 2
    first_name = 'John'
    language_code = 'en'
    await add_user(pg=pg, telegram_id=tg_user_id, level=level)

    user_init_data_raw = user_init_data(
        user_id=tg_user_id,
        first_name=first_name,
        language_code=language_code
    )

    # act
    resp = client.post(
        '/api/v1/users/get-user',
        json={
            'user_init_data': user_init_data_raw
        },
    )

    # assert
    assert resp.status_code == 200

    user = resp.json()
    assert user['telegram_id'] == tg_user_id
    assert user['level'] == level
    assert user['first_name'] == first_name
    assert user['language_code'] == language_code


async def test_get_user__invalid_hash__400(
        client: TestClient, pg: asyncpg.Pool, user_init_data: tp.Callable[..., str]
) -> None:
    # arrange
    user_init_data_raw = user_init_data(
        user_id=1,
        user_hash='invalid_hash'
    )

    # act
    resp = client.post(
        '/api/v1/users/get-user',
        json={
            'user_init_data': user_init_data_raw
        },
    )

    # assert
    assert resp.status_code == 400
