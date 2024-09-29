import typing as tp

import asyncpg
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from tests_functional.utils import add_question


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
