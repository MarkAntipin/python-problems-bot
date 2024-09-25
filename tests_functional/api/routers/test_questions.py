import asyncpg
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from settings import bot_settings
from src.api.schemas.questions import AnswerRequest
from tests_functional.utils import add_question, add_user, add_users_questions


async def test_get_question_by_id(client: TestClient, pg: asyncpg.Pool) -> None:
    question_id = await add_question(pg=pg)

    resp = client.get(
        f'/api/v1/questions/{question_id}',
    )

    assert resp.status_code == status.HTTP_200_OK

    question = resp.json()

    assert question['id'] == question_id


async def test_get_question_by_invalid_id(client: TestClient) -> None:
    invalid_question_id = 999999

    resp = client.get(f'/api/v1/questions/{invalid_question_id}')

    assert resp.status_code == status.HTTP_404_NOT_FOUND

    assert resp.json() == {"detail": "Not Found"}


async def test_get_new_random_question_for_user(client: TestClient, pg: asyncpg.Pool) -> None:
    user_level = 1
    question_id = await add_question(pg=pg, level=user_level)

    user_id = await add_user(pg=pg, level=user_level)

    resp = client.get(
        f'/api/v1/questions/user/{user_id}/level/{user_level}',
    )

    assert resp.status_code == status.HTTP_200_OK

    question = resp.json()['question']

    assert question['id'] == question_id


@pytest.mark.parametrize('answers_count, expected_result', [
    (bot_settings.MAX_QUESTION_PER_DAY, True),
    (bot_settings.MAX_QUESTION_PER_DAY - 1, False),
])
async def test_is_answered_all_questions_for_today(
    client: TestClient,
    pg: asyncpg.Pool,
    answers_count: int,
    expected_result: bool
) -> None:
    user_id = await add_user(pg=pg)

    for _ in range(answers_count):
        question_id = await add_question(pg=pg)
        await add_users_questions(pg=pg, question_id=question_id, user_id=user_id)

    resp = client.get(
        f'/api/v1/questions/user/{user_id}/answered-all',
    )

    assert resp.status_code == status.HTTP_200_OK

    assert resp.json()['is_answered_all'] == expected_result


@pytest.mark.parametrize('user_answer, question_answer, expected_result', [
    ('correct_answer', 'correct_answer', True),
    ('incorrect_answer', 'correct_answer', False),
])
async def test_answer_question(
    client: TestClient,
    pg: asyncpg.Pool,
    user_answer: str,
    question_answer:str,
    expected_result: bool
) -> None:
    question_id = await add_question(pg=pg, answer=question_answer)
    user_id = await add_user(pg=pg)

    resp = client.post(
        '/api/v1/questions/answer',
        content=AnswerRequest(
            user_id=user_id,
            question_id=question_id,
            user_answer=user_answer,
        ).model_dump_json()
    )

    assert resp.status_code == status.HTTP_200_OK

    assert resp.json()['is_correct'] == expected_result


async def test_answer_nonexistent_question(client: TestClient, pg: asyncpg.Pool) -> None:
    user_id = await add_user(pg=pg)
    invalid_question_id = 999999

    resp = client.post(
        '/api/v1/questions/answer',
        content=AnswerRequest(
            user_id=user_id,
            question_id=invalid_question_id,
            user_answer='some_answer',
        ).model_dump_json()
    )

    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json() == {"detail": "Not Found"}
