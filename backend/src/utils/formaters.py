import random

from src.models.achievements import Achievement
from src.models.questions import Question
from src.services.achievements import ACHIEVEMENTS
from src.services.advices import Advice
from src.services.leaders import Leader, UserInLeaders
from src.texts import CORRECT_ANSWERS, INCORRECT_ANSWERS

_INTERVIEW_QUESTION_PREFIX: str = 'задача с собеседования'


def _format_choices(choices: dict) -> str:
    return '\n'.join([rf'*{key.upper()}\)* {value}' for key, value in choices.items()])


def format_question(question: Question) -> str:
    formatted_choices = _format_choices(choices=question.choices)
    prefix = f">{_INTERVIEW_QUESTION_PREFIX}||\n\n" if question.from_interview else ""
    return f'{prefix}{question.text}\n\n{formatted_choices}'


def format_explanation(question: Question, is_correct: bool, user_answer: str) -> str:
    correct_answer = question.answer
    answer_text = random.choice(CORRECT_ANSWERS if is_correct else INCORRECT_ANSWERS)

    return (
        f'\n{question.text}\n\n'
        f'*Правильный ответ:* {correct_answer}\\) {question.choices[correct_answer]}\n'
        f'*Твой выбор:* {user_answer}\\) {question.choices[user_answer]}\n\n'
        f'{answer_text}\n\n'
        f'*Объяснение:*\n{question.explanation}'
    )


def format_advice(advice: Advice) -> str:
    formatted_advice = (
        f'Я понял, что тебе стоит подтянуть тему *{advice.theme}*\\.\n'
        f'Вот [ссылка]({advice.link})\n'
        r'Прочти, чтобы стать еще круче\!'
    )

    return formatted_advice


def format_achievement(achievement: Achievement) -> str:
    formatted_achievement = (
        '*У тебя новое достижение\\!* 🎉\n\n'
        f'||{achievement.text} \\- *{achievement.title}*||'
    )

    return formatted_achievement


def format_achievements_list(achievements: list[Achievement]) -> str:

    formatted_achievements = []
    for achievement in achievements:
        formatted_achievements.append(f'{achievement.text} \\- *{achievement.title}* {achievement.emoji}')

    number_of_achievements_text = f'Получено {len(formatted_achievements)} из {len(ACHIEVEMENTS)}'
    formatted_achievements_text = 'У тебя пока нет достижений 🥲'
    if formatted_achievements:
        formatted_achievements_text = '*Твои достижения:*\n\n' + '\n'.join(formatted_achievements)

    return f'{formatted_achievements_text}\n\n{number_of_achievements_text}'


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
    message_text = '*Таблица лидеров:*\n'
    score_declensions = {'accusative_many': 'баллов', 'accusative_solo': 'балла', 'nominative': 'балл'}

    for i, leader in enumerate(leaders, start=1):
        score_word = format_word_declensions(n=leader.score, declensions=score_declensions)
        user_link = f'[{leader.first_name}](https://t.me/{leader.username})'
        message_text += f'{i}\\. {user_link} \\- {leader.score} {score_word}\n'

    if user_in_leaders:
        score_word = format_word_declensions(n=user_in_leaders.score, declensions=score_declensions)
        message_text += (
            f'\n*Твое текущее место:* {user_in_leaders.position}\n'
            f'*Ты набрал* {user_in_leaders.score} {score_word}'
        )

    return message_text
