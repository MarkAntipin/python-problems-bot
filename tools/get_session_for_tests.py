from telethon.sessions import StringSession
from telethon.sync import TelegramClient

API_ID: int = 1
API_HASH: str = ''

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print('Your session string is:', client.session.save())  # noqa T201
