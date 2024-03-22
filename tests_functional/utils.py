import json
from datetime import UTC, datetime
from random import randint

import asyncpg


async def add_user(
    pg: asyncpg.Pool,
    first_name: str = 'first_name',
    last_name: str = 'last_name',
    username: str = 'username',
    payment_status: str = 'trial',
    level: int = 2,
    telegram_id: int | None = None,
    start_trial_at: datetime | None = None,
    send_payment_at: datetime | None = None,
) -> int:
    if not start_trial_at:
        start_trial_at = datetime.now(UTC)

    if not telegram_id:
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
                payment_status,
                send_payment_at,
                level
            )
        VALUES (
            $1,
            $2,
            $3,
            $4,
            $5,
            $6,
            $7,
            $8
        )
        RETURNING id;
        """,
        telegram_id,
        first_name,
        last_name,
        username,
        start_trial_at,
        payment_status,
        send_payment_at,
        level
    )
    return row['id']


async def add_question(
    pg: asyncpg.Pool,
    answer: str = 'A',
    choices: dict = None,
    text: str = 'text',
    explanation: str = 'explanation',
    level: int = 2,
    theme: str = 'lists'
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
                explanation,
                level,
                theme
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
        text,
        answer,
        json.dumps(choices),
        explanation,
        level,
        theme
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


async def add_advice(
    pg: asyncpg.Pool,
    theme: str = 'lists',
    level: int = 2,
    link: str = 'https://python.com/useful_link_to_handle_with_lists',
) -> int:
    row = await pg.fetchrow(
        """
        INSERT INTO
            advices (
                theme,
                level,
                link
            )
        VALUES (
            $1,
            $2,
            $3
        )
        RETURNING id;
        """,
        theme,
        level,
        link
    )
    return row['id']


async def add_users_send_advices(
    pg: asyncpg.Pool,
    user_id: int,
    advice_id: int,
    created_at: datetime
) -> None:
    await pg.fetchrow(
        """
        INSERT INTO
            users_send_advices (
              user_id,
              advice_id,
              created_at
            )
            VALUES (
              $1,
              $2,
              $3
            );
        """,
        user_id,
        advice_id,
        created_at
    )
