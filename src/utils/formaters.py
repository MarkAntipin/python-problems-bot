from src.services.questions import Question
from src.texts import CORRECT_ANSWER_TEXT, INCORRECT_ANSWER_TEXT


def _format_choices(choices: dict) -> str:
    return "\n".join([f"{key.upper()}) {value}" for key, value in choices.items()])


def format_question(question: Question):
    formatted_choices = _format_choices(choices=question.choices)
    return f'{question.text}\n\n{formatted_choices}'


def format_explanation(question: Question, is_correct: bool):
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
