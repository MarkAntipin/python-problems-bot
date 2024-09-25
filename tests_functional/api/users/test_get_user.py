
import asyncpg
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from tests_functional.utils import add_user


async def test_get_user(client: TestClient, pg: asyncpg.Pool, mocker: MockerFixture) -> None:
    # arrange
    user_id = 1
    first_name = 'John'
    language_code = 'en'
    level = 2
    user_hash = '4f97fa2703d6a8088bcb68eb038c7308fd5c1b6ce30874c389b03ce53f850795'
    user_init_data_raw = (
        f'user=%7B%22id%22%3A{user_id}%2C%22first_name%22%3A%22{first_name}'
        f'%22%2C%22language_code%22%3A%22{language_code}%22%7D&hash={user_hash}'
    )

    await add_user(pg=pg, telegram_id=user_id, level=level)

    mocker.patch('src.utils.user_init_data.bot_settings.TOKEN', 'token')

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
    assert user['telegram_id'] == user_id
    assert user['level'] == level
    assert user['first_name'] == first_name
    assert user['language_code'] == language_code


async def test_get_user__invalid_hash(client: TestClient, pg: asyncpg.Pool, mocker: MockerFixture) -> None:
    # arrange
    user_id = 1
    first_name = 'John'
    language_code = 'en'
    level = 2
    user_hash = 'invalid_hash'
    user_init_data_raw = (
        f'user=%7B%22id%22%3A{user_id}%2C%22first_name%22%3A%22{first_name}'
        f'%22%2C%22language_code%22%3A%22{language_code}%22%7D&hash={user_hash}'
    )

    await add_user(pg=pg, telegram_id=user_id, level=level)

    mocker.patch('src.utils.user_init_data.bot_settings.TOKEN', 'token')

    # act
    resp = client.post(
        '/api/v1/users/get-user',
        json={
            'user_init_data': user_init_data_raw
        },
    )

    # assert
    assert resp.status_code == 400
