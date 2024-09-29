import asyncpg
from pytest_mock import MockerFixture
from telegram import User as TGUser

from src.bot.handlers.payment import successful_payment_handler
from tests_functional.utils import add_question, add_user


async def test_successful_payment_handler(
    pg: asyncpg.Pool,
    mocker: MockerFixture
) -> None:
    # arrange
    user_id = await add_user(pg=pg, telegram_id=1, level=1, payment_status='trial')
    question_id = await add_question(pg=pg, level=1)

    update_mock = mocker.AsyncMock()
    update_mock.effective_user = TGUser(id=1, is_bot=False, first_name='first_name')
    await mocker.patch('src.bot.handlers.payment.pg_pool', pg)

    # act
    await successful_payment_handler(update_mock, None)

    # assert
    # check that the user payment_status was updated
    user = await pg.fetchrow("""SELECT * FROM users WHERE id = $1""", user_id)
    assert user['payment_status'] == 'paid'
    assert user['last_paid_at']

    # check that the question was sent
    assert (
        await pg.fetchrow(
            """
                SELECT * FROM users_send_questions WHERE user_id = $1 and question_id = $2
            """,
            user_id,
            question_id
        )
    )
