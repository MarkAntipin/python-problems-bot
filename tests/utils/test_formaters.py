from src.utils.formaters import format_explanation, format_question
from src.services.questions import Question


def test_format_question():
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


def test_format_explanation():
    res = format_explanation(
        question=Question(
            id=1,
            text='text',
            answer='A',
            choices={'A': 1, 'B': 2},
            explanation='explanation'
        ),
        is_correct=True
    )
    assert res == 'text\n\n<b>Ответ:</b> A) 1\n\nПравильно ✅\n\n<b> Объяснение:</b>\nexplanation'
