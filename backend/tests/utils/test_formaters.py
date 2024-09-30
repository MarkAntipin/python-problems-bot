import random
from unittest.mock import Mock

import pytest

from src.models.achievements import Achievement
from src.models.questions import Question
from src.services.achievements import ACHIEVEMENTS
from src.services.advices import Advice
from src.services.leaders import Leader, UserInLeaders
from src.utils.formaters import (
    format_achievement,
    format_achievements_list,
    format_advice,
    format_explanation,
    format_leaders_message,
    format_question,
)


@pytest.fixture
def test_question(request: pytest.FixtureRequest) -> Question:
    """A fixture for creating a test question object"""
    from_interview = request.param if hasattr(request, 'param') else False
    return Question(
        id=1,
        text='text',
        choices={'A': 1, 'B': 2},
        answer='A',
        explanation='explanation',
        from_interview=from_interview,
    )

@pytest.mark.parametrize('test_question, expected_output', [
    (False, (
        'text\n\n'
        '*A\\)* 1\n'
        '*B\\)* 2'
        )
    ),
    (True, (
        '>задача с собеседования||\n\n'
        'text\n\n'
        '*A\\)* 1\n'
        '*B\\)* 2'
        )
     )
], indirect=['test_question'])
def test_format_question(test_question: Question, expected_output: str) -> None:
    # act
    res = format_question(question=test_question)

    # assert
    assert res == expected_output

def test_format_explanation__correct_answer(test_question: Question) -> None:
    # arrange
    random.choice = Mock(return_value=r'Правильный ответ\! 👍')
    user_answer = 'A'
    is_correct = True

    # act
    result = format_explanation(test_question, is_correct, user_answer)

    # assert
    assert result == (
        "\ntext\n\n"
        "*Правильный ответ:* A\\) 1\n"
        "*Твой выбор:* A\\) 1\n\n"
        "Правильный ответ\\! 👍\n\n"
        "*Объяснение:*\n"
        "explanation"
    )


def test_format_explanation__incorrect_answer(test_question: Question) -> None:
    # arrange
    random.choice = Mock(return_value=r"Упс, мимо\! 🙊")
    user_answer = "B"
    is_correct = False

    # act
    result = format_explanation(test_question, is_correct, user_answer)

    # assert
    assert result == (
        "\ntext\n\n"
        "*Правильный ответ:* A\\) 1\n"
        "*Твой выбор:* B\\) 2\n\n"
        "Упс, мимо\\! 🙊\n\n"
        "*Объяснение:*\nexplanation"
    )


def test_format_advice() -> None:
    # act
    res = format_advice(
        advice=Advice(
            advice_id=1,
            theme='lists',
            level=1,
            link='https://python.com/useful_link_to_handle_with_lists'
        )
    )

    # assert
    assert res == (
        'Я понял, что тебе стоит подтянуть тему *lists*\\.\n'
        'Вот [ссылка](https://python.com/useful_link_to_handle_with_lists)\n'
        'Прочти, чтобы стать еще круче\\!'
    )


def test_format_achievements() -> None:
    # arrange
    achievement = Achievement(
        text='text',
        title='title',
        emoji='',
        name='',
        emoji_key=''
    )

    # act
    formatted_achievement = format_achievement(achievement=achievement)

    # assert
    assert formatted_achievement == (
        '*У тебя новое достижение\\!* 🎉\n\n'
        '||text \\- *title*||'
    )


def test_format_achievements_list() -> None:
    # arrange
    achievements = [
        Achievement(
            text='text',
            title='title',
            emoji='😀',
            name='',
            emoji_key=''
        ),
        Achievement(
            text='text2',
            title='title2',
            emoji='🤘',
            name='',
            emoji_key=''
        )
    ]

    # act
    res = format_achievements_list(achievements=achievements)

    # assert
    assert res == (
        '*Твои достижения:*\n\n'
        'text \\- *title* 😀\n'
        'text2 \\- *title2* 🤘\n\n'
        f'Получено 2 из {len(ACHIEVEMENTS)}'
    )


def test_format_achievements_list__no_achievements() -> None:
    # act
    res = format_achievements_list(achievements=[])

    # assert
    assert res == (
        'У тебя пока нет достижений 🥲\n\n'
        f'Получено 0 из {len(ACHIEVEMENTS)}'
    )


def test_format_leaders_message() -> None:
    # arrange
    leaders = [
        Leader(id=1, first_name='User1', username='user1', score=12),
        Leader(id=2, first_name='User2', username='user2', score=3),
        Leader(id=3, first_name='User3', username='user3', score=1),
    ]
    user_in_leaders = UserInLeaders(score=12, position=1)

    # act
    formatted_message = format_leaders_message(leaders=leaders, user_in_leaders=user_in_leaders)

    # assert
    assert formatted_message == (
        '*Таблица лидеров:*\n'
        '1\\. [User1](https://t.me/user1) \\- 12 баллов\n'
        '2\\. [User2](https://t.me/user2) \\- 3 балла\n'
        '3\\. [User3](https://t.me/user3) \\- 1 балл\n'
        '\n'
        '*Твое текущее место:* 1\n'
        '*Ты набрал* 12 баллов'
    )


def test_format_leaders_message__user_not_found() -> None:
    leaders = [
        Leader(id=1, first_name='User1', username='user1', score=10),
        Leader(id=2, first_name='User2', username='user2', score=20),
        Leader(id=3, first_name='User3', username='user3', score=15),
    ]

    formatted_message = format_leaders_message(leaders=leaders, user_in_leaders=None)

    expected_message = (
        '*Таблица лидеров:*\n'
        '1\\. [User1](https://t.me/user1) \\- 10 баллов\n'
        '2\\. [User2](https://t.me/user2) \\- 20 баллов\n'
        '3\\. [User3](https://t.me/user3) \\- 15 баллов\n'
    )
    assert formatted_message == expected_message
