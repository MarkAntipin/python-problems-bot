import asyncpg
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.models.questions import AnswerRequest
from tests_functional.utils import add_question


async def test_get_new_random_question_for_user(client: TestClient, pg: asyncpg.Pool, user_init_data_raw: str) -> None:
    user_level: int = 1
    question_id = await add_question(pg=pg, level=user_level)

    resp = client.post(
        '/api/v1/questions/get-new-question',
        json={
            'user_init_data': user_init_data_raw
        },
    )

    assert resp.status_code == status.HTTP_200_OK

    question = resp.json()['question']

    assert question['id'] == question_id


@pytest.mark.parametrize('user_answer, question_answer, expected_result', [
    ('correct_answer', 'correct_answer', True),
    ('incorrect_answer', 'correct_answer', False),
])
async def test_answer_question(
    client: TestClient,
    pg: asyncpg.Pool,
    user_init_data_raw: str,
    user_answer: str,
    question_answer:str,
    expected_result: bool
) -> None:
    question_id = await add_question(pg=pg, answer=question_answer)

    resp = client.post(
        '/api/v1/questions/answer',
        json=AnswerRequest(
            user_init_data=user_init_data_raw,
            question_id=question_id,
            user_answer=user_answer,
        ).model_dump()
    )

    assert resp.status_code == status.HTTP_200_OK

    assert resp.json()['is_correct'] == expected_result


async def test_answer_nonexistent_question(
    client: TestClient,
    pg: asyncpg.Pool,
    user_init_data_raw: str
) -> None:
    invalid_question_id: int = 999999

    resp = client.post(
        '/api/v1/questions/answer',
        json=AnswerRequest(
            user_init_data=user_init_data_raw,
            question_id=invalid_question_id,
            user_answer='some_answer',
        ).model_dump()
    )

    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    assert resp.json() == {"detail": f'Not found question with id - {invalid_question_id}'}
