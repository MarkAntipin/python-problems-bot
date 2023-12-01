from src.services.leaders import Leader, UserInLeaders
from src.services.questions import Question
from src.services.advices import Advice
from src.texts import CORRECT_ANSWER_TEXT, INCORRECT_ANSWER_TEXT


def _format_choices(choices: dict) -> str:
    return '\n'.join([f'{key.upper()}) {value}' for key, value in choices.items()])


def format_question(question: Question) -> str:
    formatted_choices = _format_choices(choices=question.choices)
    return f'{question.text}\n\n{formatted_choices}'


def format_explanation(question: Question, is_correct: bool) -> str:
    if is_correct:
        answer_text = CORRECT_ANSWER_TEXT
    else:
        answer_text = INCORRECT_ANSWER_TEXT

    return (
        f'{question.text}\n\n'
        f'<b>Ответ:</b> {question.answer})'
        f' {question.choices[question.answer]}\n\n'
        f'{answer_text}'
        f'<b> Объяснение:</b>\n'
        f'{question.explanation}'
    )


def format_advice(advice: Advice) -> str:
    themes = {
        'lists': 'Списки',
        'strings': 'Строки',
        'functions': 'Функции'
    }

    formatted_advice = f'Я понял, что тебе стоит подтянуть тему "{themes[advice.theme]}".\n' \
                       f'Вот ссылка: {advice.link}\n' \
                       f'Прочти, чтобы стать еще круче!\n\n' \
                       f'Не забудь оставить фидбэк 👇'

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
