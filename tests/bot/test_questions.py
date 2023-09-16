import pytest
from asyncio import sleep
import asyncpg
from telethon.custom import Conversation
import json


async def _add_question(
    pg: asyncpg.Connection,
    answer: str = 'A',
    choices: dict = None,
    text: str = 'text',
    explanation: str = 'explanation'
):
    if not choices:
        choices = {'A': 1, 'B': 2, 'C': 3}
    await pg.execute(
        """
        INSERT INTO
            questions (
                text,
                answer,
                choices,
                explanation
            )
        VALUES (
            $1,
            $2,
            $3, 
            $4
        );
        """,
        text,
        answer,
        json.dumps(choices),
        explanation
    )


@pytest.mark.asyncio
async def test_questions__no_question(
        conv: Conversation,
        sleep_for_between_actions: float
):
    # act
    await sleep(sleep_for_between_actions)
    await conv.send_message('/start')

    resp = await conv.get_response()

    # press the button
    await sleep(sleep_for_between_actions)
    await resp.click(i=0, j=0)

    await sleep(sleep_for_between_actions)

    resp = await conv.get_response()

    # assert
    assert resp.raw_text
    assert not resp.photo


@pytest.mark.asyncio
async def test_questions__correct_answer_questions(
        conv: Conversation,
        pg: asyncpg.Connection,
        sleep_for_between_actions: float
):
    # arrange

    _answer = 'A'
    _text = 'text'
    _explanation = 'explanation'
    await _add_question(pg=pg, answer=_answer, text=_text, explanation=_explanation)

    # act
    await sleep(sleep_for_between_actions)
    await conv.send_message('/start')

    resp = await conv.get_response()

    # press the button
    await sleep(sleep_for_between_actions)
    await resp.click(i=0, j=0)

    await sleep(sleep_for_between_actions)

    # get question
    resp = await conv.get_response()
    assert resp.raw_text == 'text\n\nA) 1\nB) 2\nC) 3'

    # answer on question
    await sleep(sleep_for_between_actions)
    await resp.click(text=_answer)

    resp = await conv.get_response()
    assert resp.raw_text
