import random

from src.services.advices import Advice
from src.services.leaders import Leader, UserInLeaders
from src.services.questions import Question
from src.texts import CORRECT_ANSWERS, INCORRECT_ANSWERS


def _format_choices(choices: dict) -> str:
    return '\n'.join([f'{key.upper()}) {value}' for key, value in choices.items()])


def format_question(question: Question) -> str:
    formatted_choices = _format_choices(choices=question.choices)
    return f'{question.text}\n\n{formatted_choices}'


def format_explanation(question: Question, is_correct: bool, user_answer: str) -> str:
    user_choice = question.answer if is_correct else user_answer
    answer_text = random.choice(CORRECT_ANSWERS if is_correct else INCORRECT_ANSWERS)
    _q_choice = f'{question.choices[question.answer]}\n'
    explanation = f'<b> Объяснение:</b>\n{question.explanation}' if not is_correct else ''

    return (
        f'\n{question.text}\n'
        f'{answer_text}\n'
        f'<b>Правильный ответ:</b> {question.answer}) {_q_choice}'
        f'<b>Твой выбор:</b> {user_choice})\n'
        f'{explanation}'
    )


def format_advice(advice: Advice) -> str:
    formatted_advice = f'Я понял, что тебе стоит подтянуть тему "{advice.theme}".\n' \
                       f'Вот <a href="{advice.link}">ссылка</a>\n' \
                       f'Прочти, чтобы стать еще круче!'

    return formatted_advice


def format_word_declensions(n: int, declensions: dict[str, str]) -> str:
    units = n % 10
    tens = (n // 10) % 10
    if tens == 1:
        return declensions['accusative_many']
    if units in [0, 5, 6, 7, 8, 9]:
        return declensions['accusative_many']
    if units == 1:
        return declensions['nominative']
    if units in [2, 3, 4]:
        return declensions['accusative_solo']


def format_leaders_message(leaders: list[Leader], user_in_leaders: UserInLeaders | None) -> str:
    message_text = '<b>Таблица лидеров:</b>\n'
    score_declensions = {'accusative_many': 'баллов', 'accusative_solo': 'балла', 'nominative': 'балл'}

    for i, leader in enumerate(leaders, start=1):
        score_word = format_word_declensions(n=leader.score, declensions=score_declensions)
        user_link = f'<a href="https://t.me/{leader.username}">{leader.first_name}</a>'
        message_text += f'{i}. {user_link} - {leader.score} {score_word}\n'

    if user_in_leaders:
        score_word = format_word_declensions(n=user_in_leaders.score, declensions=score_declensions)
        message_text += (
            f'\n<b>Ваше текущее место:</b> {user_in_leaders.position}.'
            f' Вы набрали {user_in_leaders.score} {score_word}.'
        )

    return message_text
