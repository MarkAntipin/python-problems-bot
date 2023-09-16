import pytest

from src.utils.telegram.callback_data import parse_callback_questions_data, ParsedCallbackQuestionsData


@pytest.mark.parametrize(
    'callback_data,res',
    [
        (None, None),
        ('', None),
        ('B_1', ParsedCallbackQuestionsData(question_id=1, answer='B')),
        ('B', None),
    ]
)
def test_parse_callback_questions_data(callback_data, res):
    parsed_callback_questions_data = parse_callback_questions_data(callback_data=callback_data)
    assert parsed_callback_questions_data == res
