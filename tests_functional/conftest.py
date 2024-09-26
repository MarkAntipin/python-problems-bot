import asyncpg
import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from settings import TestSettings
from tests_functional.utils import add_user

test_settings = TestSettings()


@pytest.fixture(name='pg')
async def pg_fixture() -> asyncpg.Connection:
    conn = await asyncpg.create_pool(
        dsn=f'postgresql://{test_settings.PG_USER}:{test_settings.PG_PASSWORD}'
        f'@{test_settings.PG_HOST}:{test_settings.PG_PORT}/{test_settings.PG_DATABASE}'
    )

    async def teardown() -> None:
        await conn.execute('DELETE FROM users_questions;')
        await conn.execute('DELETE FROM users_send_questions;')
        await conn.execute('DELETE FROM questions;')
        await conn.execute('DELETE FROM users_send_advices;')
        await conn.execute('DELETE FROM advices;')
        await conn.execute('DELETE FROM users;')
        await conn.execute('DELETE FROM users_achievements;')

    await teardown()

    yield conn

    await teardown()
    await conn.close()


@pytest.fixture(autouse=True)
async def env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('TOKEN', '')
    monkeypatch.setenv('PAYMENT_PROVIDER_TOKEN', '')

    monkeypatch.setenv('PG_HOST', test_settings.PG_HOST)
    monkeypatch.setenv('PG_PORT', str(test_settings.PG_PORT))
    monkeypatch.setenv('PG_USER', test_settings.PG_USER)
    monkeypatch.setenv('PG_PASSWORD', test_settings.PG_PASSWORD)
    monkeypatch.setenv('PG_DATABASE', test_settings.PG_DATABASE)
    monkeypatch.setenv('ENABLE_PAYMENT', '1')


@pytest.fixture()
async def client() -> TestClient:
    from run_app import app
    with TestClient(app=app) as client:
        yield client


@pytest.fixture
async def user_init_data_raw(pg: asyncpg.Pool, mocker: MockerFixture) -> str:
    user_id = 1
    first_name = 'John'
    language_code = 'en'
    user_level = 1
    user_hash = '4f97fa2703d6a8088bcb68eb038c7308fd5c1b6ce30874c389b03ce53f850795'

    user_init_data_raw = (
        f'user=%7B%22id%22%3A{user_id}%2C%22first_name%22%3A%22{first_name}'
        f'%22%2C%22language_code%22%3A%22{language_code}%22%7D&hash={user_hash}'
    )

    await add_user(pg=pg, telegram_id=user_id, level=user_level)

    mocker.patch('src.utils.user_init_data.bot_settings.TOKEN', 'token')

    return user_init_data_raw
