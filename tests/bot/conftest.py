import pytest
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncpg
import pytest_asyncio
from telethon.custom import Conversation

from settings import TestSettings


test_settings = TestSettings()


@pytest.fixture()
def sleep_for_between_actions() -> float:
    return 0.5


@pytest_asyncio.fixture
async def client() -> TelegramClient:
    async with TelegramClient(
        StringSession(test_settings.TELETHON_SESSION),
        test_settings.TELEGRAM_APP_ID,
        test_settings.TELEGRAM_APP_HASH,
        sequential_updates=True
    ) as client:
        yield client


@pytest_asyncio.fixture
async def conv(client) -> Conversation:
    async with client.conversation(test_settings.BOT_NAME) as conv:
        yield conv


@pytest_asyncio.fixture
async def pg() -> asyncpg.Connection:
    conn = await asyncpg.connect(
        f'postgresql://{test_settings.PG_USER}:{test_settings.PG_PASSWORD}'
        f'@{test_settings.PG_HOST}:{test_settings.PG_PORT}/{test_settings.PG_DATABASE}'
    )

    async def teardown():
        await conn.execute('DELETE FROM users_questions;')
        await conn.execute('DELETE FROM questions;')
        await conn.execute('DELETE FROM users;')

    await teardown()

    yield conn

    await teardown()
