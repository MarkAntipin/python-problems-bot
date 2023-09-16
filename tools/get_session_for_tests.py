from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID: int = 1
API_HASH: str = ''

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print('Your session string is:', client.session.save())
