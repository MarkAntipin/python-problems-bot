import typing as tp

import asyncpg
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from settings import bot_settings
from tests_functional.utils import add_question, add_user, add_user_send_question


async def test_get_new_random_question_for_user__ok(
    client: TestClient,
    pg: asyncpg.Pool,
    user_init_data: tp.Callable[..., str]
) -> None:
    # arrange
    tg_user_id: int = 1
    user_level: int = 1
    await add_user(pg=pg, level=user_level, telegram_id=tg_user_id)
    question_id = await add_question(pg=pg, level=user_level)
    user_init_data_raw = user_init_data(user_id=tg_user_id)

    # act
    resp = client.post(
        '/api/v1/questions/get-new-question',
        json={
            'user_init_data': user_init_data_raw
        },
    )

    # assert
    assert resp.status_code == status.HTTP_200_OK

    question = resp.json()

    assert question['id'] == question_id


async def test_get_new_random_question_for_user__no_questions_for_today__400(
    client: TestClient,
    pg: asyncpg.Pool,
    user_init_data: tp.Callable[..., str]
) -> None:
    # arrange
    tg_user_id: int = 1
    user_init_data_raw = user_init_data(user_id=tg_user_id)
    user_id = await add_user(pg=pg, telegram_id=tg_user_id)

    # arrange
    for _ in range(bot_settings.MAX_QUESTION_PER_DAY + 1):
        question_id = await add_question(pg=pg)
        await add_user_send_question(
            pg=pg,
            question_id=question_id,
            user_id=user_id
        )

    # act
    resp = client.post(
        '/api/v1/questions/get-new-question',
        json={
            'user_init_data': user_init_data_raw
        },
    )

    # assert
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize('user_answer, question_answer, expected_result', [
    ('correct_answer', 'correct_answer', True),
    ('incorrect_answer', 'correct_answer', False),
])
async def test_answer_question__ok(
    client: TestClient,
    pg: asyncpg.Pool,
    user_init_data: tp.Callable[..., str],
    user_answer: str,
    question_answer: str,
    expected_result: bool
) -> None:
    # arrange
    tg_user_id: int = 1
    user_init_data_raw = user_init_data(user_id=tg_user_id)
    question_id = await add_question(pg=pg, answer=question_answer)

    # act
    resp = client.post(
        '/api/v1/questions/answer',
        json={
            'user_init_data': user_init_data_raw,
            'question_id': question_id,
            'user_answer': user_answer,
        }
    )

    # assert
    assert resp.status_code == status.HTTP_200_OK

    assert resp.json()['is_correct'] == expected_result


async def test_answer_question__question_not_found(
    client: TestClient,
    user_init_data: tp.Callable[..., str]
) -> None:
    # arrange
    invalid_question_id: int = 999999
    user_init_data_raw = user_init_data()

    # act
    resp = client.post(
        '/api/v1/questions/answer',
        json={
            'user_init_data': user_init_data_raw,
            'question_id': invalid_question_id,
            'user_answer': 'some_answer',
        }
    )

    # assert
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    assert resp.json() == {"detail": f'Not found question with id - {invalid_question_id}'}
