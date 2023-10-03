import json
from datetime import UTC, datetime
from random import randint

import asyncpg


async def add_user(
    pg: asyncpg.Pool,
    first_name: str = 'first_name',
    last_name: str = 'last_name',
    username: str = 'username',
) -> int:
    telegram_id = randint(0, 100000)
    row = await pg.fetchrow(
        """
        INSERT INTO
            users (
                telegram_id,
                first_name,
                last_name,
                username,
                start_trial_at,
                payment_status
            )
        VALUES (
            $1,
            $2,
            $3,
            $4,
            $5,
            $6
        )
        RETURNING id;
        """,
        telegram_id,
        first_name,
        last_name,
        username,
        datetime.now(UTC),
        'trial'
    )
    return row['id']


async def add_question(
    pg: asyncpg.Pool,
    answer: str = 'A',
    choices: dict = None,
    text: str = 'text',
    explanation: str = 'explanation'
) -> int:
    if not choices:
        choices = {'A': 1, 'B': 2, 'C': 3}
    row = await pg.fetchrow(
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
        )
        RETURNING id;
        """,
        text,
        answer,
        json.dumps(choices),
        explanation
    )
    return row['id']


async def add_users_questions(
    pg: asyncpg.Pool,
    question_id: int,
    user_id: int,
    is_correct: bool = True,
    answer: str = 'answer',
) -> None:
    await pg.execute(
        """
        INSERT INTO
            users_questions (
                answer,
                question_id,
                user_id,
                is_correct
            )
        VALUES (
            $1,
            $2,
            $3,
            $4
        );
        """,
        answer,
        question_id,
        user_id,
        is_correct
    )
