from asyncio import sleep

import asyncpg
import pytest

from telethon.custom import Conversation


@pytest.mark.asyncio
async def test_start(
        conv: Conversation,
        sleep_for_between_actions: float,
        pg: asyncpg.Connection
):
    # act
    await sleep(sleep_for_between_actions)
    await conv.send_message('/start')

    resp = await conv.get_response()

    # assert
    # user created in db
    user = await pg.fetchrow('SELECT * from users')
    assert user

    assert resp.raw_text
    assert resp.photo
    assert resp.buttons
    assert resp.buttons[0][0].text == 'Поехали 🚀'
