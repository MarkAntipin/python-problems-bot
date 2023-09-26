from src.repositories.postgres.leaders import LeadersRepo
from src.services.questions import Question
from src.services.users import User
from src.services.leaders import Leader
from src.texts import CORRECT_ANSWER_TEXT, INCORRECT_ANSWER_TEXT


def _format_choices(choices: dict) -> str:
    return "\n".join([f"{key.upper()}) {value}" for key, value in choices.items()])


def format_question(question: Question) -> str:
    formatted_choices = _format_choices(choices=question.choices)
    return f'{question.text}\n\n{formatted_choices}'


def format_explanation(question: Question, is_correct: bool) -> str:
    if is_correct:
        answer_text = CORRECT_ANSWER_TEXT
    else:
        answer_text = INCORRECT_ANSWER_TEXT

    return (
        f"{question.text}\n\n"
        f"<b>Ответ:</b> {question.answer})"
        f" {question.choices[question.answer]}\n\n"
        f"{answer_text}"
        f"<b> Объяснение:</b>\n"
        f"{question.explanation}"
    )


def format_leaders_message(leaders: list[Leader], user_position: int, user_score: int) -> str:
    message_text = '<b>Таблица лидеров:</b>\n'
    for i, leader in enumerate(leaders, start=1):
        user_link = f'<a href="https://t.me/{leader.username}">{leader.first_name}</a>'
        message_text += f"{i}. {user_link} - {leader.score} баллов\n"

    message_text += f"\n<b>Ваше текущее место:</b> {user_position}. Вы набрали {user_score} баллов."

    return message_text
