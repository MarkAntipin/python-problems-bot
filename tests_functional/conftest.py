import asyncpg
import pytest

from settings import TestSettings

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

    await teardown()

    yield conn

    await teardown()


@pytest.fixture(autouse=True)
async def env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('PG_HOST', '')
    monkeypatch.setenv('PG_USER', '')
    monkeypatch.setenv('PG_PASSWORD', '')
    monkeypatch.setenv('PG_DATABASE', '')
    monkeypatch.setenv('PG_PORT', '')
    monkeypatch.setenv('TOKEN', '')
