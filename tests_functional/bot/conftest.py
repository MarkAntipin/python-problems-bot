import pytest
import pytest_asyncio
from telethon import TelegramClient
from telethon.custom import Conversation
from telethon.sessions import StringSession

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
async def conv(client: TelegramClient) -> Conversation:
    async with client.conversation(test_settings.BOT_NAME) as conv:
        yield conv
