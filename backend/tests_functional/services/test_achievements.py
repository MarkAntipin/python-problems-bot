import asyncpg

from src.services.achievements import AchievementsService
from tests_functional.utils import add_question, add_user, add_user_achievement, add_users_questions


async def test_check_for_new_achievements(
    pg: asyncpg.Pool,
) -> None:
    # arrange
    user_id = await add_user(pg=pg)
    question_id_1 = await add_question(pg=pg)

    # already have first_correct_answer achievement
    await add_user_achievement(pg=pg, user_id=user_id, achievement_name='first_correct_answer')

    # incorrect answer
    await add_users_questions(pg=pg, question_id=question_id_1, user_id=user_id, is_correct=False)

    # act
    service = AchievementsService(pg_pool=pg)
    res = await service.check_for_new_achievements(user_id=user_id)

    # assert
    achievement_names = [r.name for r in res]
    assert 'first_incorrect_answer' in achievement_names
    assert 'first_correct_answer' not in achievement_names
