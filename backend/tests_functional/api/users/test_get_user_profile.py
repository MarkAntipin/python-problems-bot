import typing as tp

import asyncpg
from fastapi.testclient import TestClient

from tests_functional.utils import add_user, add_user_achievement


async def test_get_user_profile__ok(
    client: TestClient,
    pg: asyncpg.Pool,
    user_init_data: tp.Callable[..., str]
) -> None:
    # arrange
    tg_user_id = 1
    level = 2
    first_name = 'John'
    language_code = 'en'
    user_id = await add_user(pg=pg, telegram_id=tg_user_id, level=level)

    user_init_data_raw = user_init_data(
        user_id=tg_user_id,
        first_name=first_name,
        language_code=language_code
    )

    await add_user_achievement(pg=pg, user_id=user_id, achievement_name='solve_10_loops_questions')

    # act
    resp = client.post(
        '/api/v1/users/get-user-profile',
        json={
            'user_init_data': user_init_data_raw
        },
    )

    # assert
    assert resp.status_code == 200

    user_profile = resp.json()

    assert len(user_profile['achievements']) == 1
    assert user_profile['user_position'] == 1


async def test_get_user_profile__invalid_hash__400(
    client: TestClient,
    user_init_data: tp.Callable[..., str]
) -> None:
    # arrange
    user_init_data_raw = user_init_data(
        user_id=1,
        user_hash='invalid_hash'
    )

    # act
    resp = client.post(
        '/api/v1/users/get-user-profile',
        json={
            'user_init_data': user_init_data_raw
        },
    )

    # assert
    assert resp.status_code == 400
