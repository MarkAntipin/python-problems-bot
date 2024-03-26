import random
from unittest.mock import Mock

import pytest

from src.services.advices import Advice
from src.services.leaders import Leader, UserInLeaders
from src.services.questions import Question
from src.utils.formaters import format_advice, format_explanation, format_leaders_message, format_question


def test_format_question() -> None:
    res = format_question(
        question=Question(
            id=1,
            text='text',
            answer='A',
            choices={'A': 1, 'B': 2},
            explanation='explanation'
        )
    )
    assert res == 'text\n\nA) 1\nB) 2'


@pytest.fixture
def test_question() -> Question:
    """A fixture for creating a test question object"""
    return Question(
        id=1,
        text='text',
        choices={'A': 1, 'B': 2},
        answer='A',
        explanation='explanation'
    )


def test_format_explanation__correct_answer(test_question: Question) -> None:
    """A test for the correct answer."""
    mock_choice = Mock(return_value="Правильный ответ! 👍")
    random.choice = mock_choice
    user_answer = "A"
    is_correct = True
    expected_output = (
        "\ntext\n"
        "Правильный ответ! 👍\n"
        "<b>Правильный ответ:</b> A) 1\n"
        "<b>Твой выбор:</b> A)\n"
        "<b> Объяснение:</b>\nexplanation"
    )
    result = format_explanation(test_question, is_correct, user_answer)
    assert result == expected_output


def test_format_explanation__incorrect_answer(test_question: Question) -> None:
    """A test for the incorrect answer."""
    mock_choice = Mock(return_value="Упс, мимо! 🙊")
    random.choice = mock_choice
    user_answer = "B"
    is_correct = False
    expected_output = (
        "\ntext\n"
        "Упс, мимо! 🙊\n"
        "<b>Правильный ответ:</b> A) 1\n"
        "<b>Твой выбор:</b> B)\n"
        "<b> Объяснение:</b>\nexplanation"
    )
    result = format_explanation(test_question, is_correct, user_answer)
    assert result == expected_output


def test_format_advice() -> None:
    res = format_advice(
        advice=Advice(
            advice_id=1,
            theme='lists',
            level=1,
            link='https://python.com/useful_link_to_handle_with_lists'
        )
    )

    assert res == 'Я понял, что тебе стоит подтянуть тему "lists".\n' \
                  'Вот <a href="https://python.com/useful_link_to_handle_with_lists">ссылка</a>\n' \
                  'Прочти, чтобы стать еще круче!'


def test_format_leaders_message() -> None:
    leaders = [
        Leader(id=1, first_name='User1', username='user1', score=12),
        Leader(id=2, first_name='User2', username='user2', score=3),
        Leader(id=3, first_name='User3', username='user3', score=1),
    ]
    user_in_leaders = UserInLeaders(score=12, position=1)

    formatted_message = format_leaders_message(leaders=leaders, user_in_leaders=user_in_leaders)

    expected_message = (
        '<b>Таблица лидеров:</b>\n'
        '1. <a href="https://t.me/user1">User1</a> - 12 баллов\n'
        '2. <a href="https://t.me/user2">User2</a> - 3 балла\n'
        '3. <a href="https://t.me/user3">User3</a> - 1 балл\n'
        '\n'
        '<b>Ваше текущее место:</b> 1. Вы набрали 12 баллов.'
    )
    assert formatted_message == expected_message


def test_format_leaders_message__user_not_found() -> None:
    leaders = [
        Leader(id=1, first_name='User1', username='user1', score=10),
        Leader(id=2, first_name='User2', username='user2', score=20),
        Leader(id=3, first_name='User3', username='user3', score=15),
    ]

    formatted_message = format_leaders_message(leaders=leaders, user_in_leaders=None)

    expected_message = (
        '<b>Таблица лидеров:</b>\n'
        '1. <a href="https://t.me/user1">User1</a> - 10 баллов\n'
        '2. <a href="https://t.me/user2">User2</a> - 20 баллов\n'
        '3. <a href="https://t.me/user3">User3</a> - 15 баллов\n'
    )
    assert formatted_message == expected_message
