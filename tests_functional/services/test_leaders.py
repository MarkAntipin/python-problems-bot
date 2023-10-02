import asyncpg

from src.services.leaders import LeadersService
from tests_functional.utils import add_question, add_user, add_users_questions


async def test_get_top_users__no_users_in_db(
    pg: asyncpg.Pool,
) -> None:
    # act
    service = LeadersService(pg_pool=pg)
    res = await service.get_top_users(limit=3)

    # assert
    assert res is None


async def test_get_top_users(
        pg: asyncpg.Pool,
) -> None:
    # arrange
    question_id_1 = await add_question(pg=pg)
    question_id_2 = await add_question(pg=pg)
    user_id_1 = await add_user(pg=pg, username='user_1')
    user_id_2 = await add_user(pg=pg, username='user_2')

    await add_users_questions(pg=pg, question_id=question_id_1, user_id=user_id_1, is_correct=True)
    await add_users_questions(pg=pg, question_id=question_id_2, user_id=user_id_1, is_correct=True)

    await add_users_questions(pg=pg, question_id=question_id_1, user_id=user_id_2, is_correct=True)
    await add_users_questions(pg=pg, question_id=question_id_2, user_id=user_id_2, is_correct=False)

    # act
    service = LeadersService(pg_pool=pg)
    res = await service.get_top_users(limit=3)

    # assert
    # 2 users in leaderboard
    assert len(res) == 2

    # check users scores
    user_1_in_leaderboard = [r for r in res if r.username == 'user_1'][0]
    assert user_1_in_leaderboard.score == 2

    user_2_in_leaderboard = [r for r in res if r.username == 'user_2'][0]
    assert user_2_in_leaderboard.score == 1

    # check users order
    assert [r.username for r in res] == ['user_1', 'user_2']
