from datetime import UTC, datetime, timedelta
from unittest.mock import Mock

import pytest

from src.models.achievements import Achievement
from src.services.achievements import AchievementsService, SolvedQuestion


@pytest.mark.parametrize(
    'solved_questions, is_achievement_unlocked',
    [
        # not enough questions
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))],
            False
        ),
        # no questions with different levels
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 10,
            False
        ),
        # no questions with different levels solved
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=False, created_at=datetime.now(UTC))] * 10 +
            [SolvedQuestion(level=2, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 10,
            False
        ),
        # by 10 questions with different levels
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 10 +
            [SolvedQuestion(level=2, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 10,
            True
        ),
    ]
)
def test_check_for_new_achievements__solve_10_different_level_questions(
        solved_questions: list[SolvedQuestion],
        is_achievement_unlocked: bool
) -> None:
    # arrange
    achievements_service = AchievementsService(pg_pool=Mock())
    achievement_name = 'solve_10_different_level_questions'

    # act
    achievements: list[Achievement] = achievements_service._check_for_new_achievements(
        solved_questions=solved_questions,
        user_current_achievements=set()
    )

    # assert
    achievement_names = [achievement.name for achievement in achievements]
    if is_achievement_unlocked:
        assert achievement_name in achievement_names
    else:
        assert achievement_name not in achievement_names


@pytest.mark.parametrize(
    'solved_questions, is_achievement_unlocked',
    [
        # not enough questions
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 49,
            False
        ),
        # not enough correct answers
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 39 +
            [SolvedQuestion(level=1, theme='lists', is_correct=False, created_at=datetime.now(UTC))] * 11,
            False
        ),
        # correct
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 65 +
            [SolvedQuestion(level=1, theme='lists', is_correct=False, created_at=datetime.now(UTC))] * 11,
            True
        ),
    ]
)
def test_check_for_new_achievements__less_than_20_percent_errors_in_50_questions(
        solved_questions: list[SolvedQuestion],
        is_achievement_unlocked: bool
) -> None:
    # arrange
    achievements_service = AchievementsService(pg_pool=Mock())
    achievement_name = 'less_than_20_percent_errors_in_50_questions'

    # act
    achievements: list[Achievement] = achievements_service._check_for_new_achievements(
        solved_questions=solved_questions,
        user_current_achievements=set()
    )

    # assert
    achievement_names = [achievement.name for achievement in achievements]
    if is_achievement_unlocked:
        assert achievement_name in achievement_names
    else:
        assert achievement_name not in achievement_names


@pytest.mark.parametrize(
    'solved_questions, is_achievement_unlocked',
    [
        # not enough questions
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 2,
            False
        ),
        # came back after 2 days
        (
            [
                SolvedQuestion(
                    level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC) - timedelta(days=2)
                )
            ] * 3 +
            [SolvedQuestion(level=1, theme='lists', is_correct=False, created_at=datetime.now(UTC))],
            False
        ),
        # came back after 3 days
        (
            [
                SolvedQuestion(
                    level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC) - timedelta(days=3)
                )
            ] * 3 +
            [SolvedQuestion(level=1, theme='lists', is_correct=False, created_at=datetime.now(UTC))],
            True
        ),
    ]
)
def test_check_for_new_achievements__comeback_after_3_days(
        solved_questions: list[SolvedQuestion],
        is_achievement_unlocked: bool
) -> None:
    # arrange
    achievements_service = AchievementsService(pg_pool=Mock())
    achievement_name = 'comeback_after_3_days'

    # act
    achievements: list[Achievement] = achievements_service._check_for_new_achievements(
        solved_questions=solved_questions,
        user_current_achievements=set()
    )

    # assert
    achievement_names = [achievement.name for achievement in achievements]
    if is_achievement_unlocked:
        assert achievement_name in achievement_names
    else:
        assert achievement_name not in achievement_names


@pytest.mark.parametrize(
    'solved_questions, is_achievement_unlocked',
    [
        # not enough questions
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 2,
            False
        ),
        # not enough correct answers
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 25 +
            [SolvedQuestion(level=1, theme='lists', is_correct=False, created_at=datetime.now(UTC))] * 5,
            False
        ),
        # correct
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 27,
            True
        ),
    ]
)
def test_check_for_new_achievements__solve_27_questions(
        solved_questions: list[SolvedQuestion],
        is_achievement_unlocked: bool
) -> None:
    # arrange
    achievements_service = AchievementsService(pg_pool=Mock())
    achievement_name = 'solve_27_questions'

    # act
    achievements: list[Achievement] = achievements_service._check_for_new_achievements(
        solved_questions=solved_questions,
        user_current_achievements=set()
    )

    # assert
    achievement_names = [achievement.name for achievement in achievements]
    if is_achievement_unlocked:
        assert achievement_name in achievement_names
    else:
        assert achievement_name not in achievement_names


@pytest.mark.parametrize(
    'solved_questions, is_achievement_unlocked',
    [
        # not enough questions
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 9,
            False
        ),
        # not enough incorrect answers
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 19 +
            [SolvedQuestion(level=1, theme='lists', is_correct=False, created_at=datetime.now(UTC))] * 1,
            False
        ),
        # enough incorrect answers
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=False, created_at=datetime.now(UTC))] * 10,
            True
        ),
    ]
)
def test_check_for_new_achievements__solve_10_incorrect_questions(
        solved_questions: list[SolvedQuestion],
        is_achievement_unlocked: bool
) -> None:
    # arrange
    achievements_service = AchievementsService(pg_pool=Mock())
    achievement_name = 'solve_10_incorrect_questions'

    # act
    achievements: list[Achievement] = achievements_service._check_for_new_achievements(
        solved_questions=solved_questions,
        user_current_achievements=set()
    )

    # assert
    achievement_names = [achievement.name for achievement in achievements]
    if is_achievement_unlocked:
        assert achievement_name in achievement_names
    else:
        assert achievement_name not in achievement_names


@pytest.mark.parametrize(
    'solved_questions, is_achievement_unlocked',
    [
        # solve 2 questions in a row
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 2,
            False
        ),
        # solve 2 questions and after incorrect in a row
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 2 +
            [SolvedQuestion(level=1, theme='lists', is_correct=False, created_at=datetime.now(UTC))] +
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))],
            False
        ),
        #  solve 3 questions in a row
        (
            [SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 3,
            True
        ),
    ]
)
def test_check_for_new_achievements__solve_3_questions_in_a_row(
        solved_questions: list[SolvedQuestion],
        is_achievement_unlocked: bool
) -> None:
    # arrange
    achievements_service = AchievementsService(pg_pool=Mock())
    achievement_name = 'solve_3_questions_in_a_row'

    # act
    achievements: list[Achievement] = achievements_service._check_for_new_achievements(
        solved_questions=solved_questions,
        user_current_achievements=set()
    )

    # assert
    achievement_names = [achievement.name for achievement in achievements]
    if is_achievement_unlocked:
        assert achievement_name in achievement_names
    else:
        assert achievement_name not in achievement_names


@pytest.mark.parametrize(
    'solved_questions, is_achievement_unlocked',
    [
        # solve 9 days in a row
        (
            [
                SolvedQuestion(
                    level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC) - timedelta(days=i)
                )
                for i in range(9)
            ],
            False
        ),
        # solve 10 days in a row
        (
            [
                SolvedQuestion(
                    level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC) - timedelta(days=i)
                )
                for i in range(10)
            ],
            True
        ),
    ]
)
def test_check_for_new_achievements__solve_questions_10_days_in_a_row(
        solved_questions: list[SolvedQuestion],
        is_achievement_unlocked: bool
) -> None:
    # arrange
    achievements_service = AchievementsService(pg_pool=Mock())
    achievement_name = 'solve_questions_10_days_in_a_row'

    # act
    achievements: list[Achievement] = achievements_service._check_for_new_achievements(
        solved_questions=solved_questions,
        user_current_achievements=set()
    )

    # assert
    achievement_names = [achievement.name for achievement in achievements]
    if is_achievement_unlocked:
        assert achievement_name in achievement_names
    else:
        assert achievement_name not in achievement_names


def test_check_for_new_achievements__without_user_current_achievements() -> None:
    # arrange
    achievements_service = AchievementsService(pg_pool=Mock())

    # act
    achievements: list[Achievement] = achievements_service._check_for_new_achievements(
        solved_questions=[SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))] * 10,
        user_current_achievements={'first_correct_answer'}
    )

    # assert
    achievement_names = [achievement.name for achievement in achievements]
    assert 'first_correct_answer' not in achievement_names
    assert 'solve_10_questions' in achievement_names


@pytest.mark.parametrize(
    'solved_questions, is_achievement_unlocked',
    [
        # solve 10 loops questions
        (
            [
                SolvedQuestion(level=1, theme='loops', is_correct=True, created_at=datetime.now(UTC))
            ] * 10,
            True
        ),
        # solve 10 days in a row
        (
            [
                SolvedQuestion(level=1, theme='lists', is_correct=True, created_at=datetime.now(UTC))
            ] * 10,
            False
        ),
    ]
)
def test_check_for_new_achievements__solve_10_loops_questions(
    solved_questions: list[SolvedQuestion],
    is_achievement_unlocked: bool
) -> None:
    # arrange
    achievements_service = AchievementsService(pg_pool=Mock())
    achievement_name = 'solve_10_loops_questions'

    # act
    achievements: list[Achievement] = achievements_service._check_for_new_achievements(
        solved_questions=solved_questions,
        user_current_achievements=set()
    )

    # assert
    achievement_names = [achievement.name for achievement in achievements]
    if is_achievement_unlocked:
        assert achievement_name in achievement_names
    else:
        assert achievement_name not in achievement_names
