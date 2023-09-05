from pydantic import BaseModel

_CALLBACK_DATA_DELIMITER = '_'


class ParsedCallbackQuestionsData(BaseModel):
    question_id: int
    answer: str


def parse_callback_questions_data(callback_data: str | None) -> ParsedCallbackQuestionsData | None:
    if not callback_data:
        return

    _callback_data = callback_data.split(_CALLBACK_DATA_DELIMITER)
    if len(_callback_data) != 2:
        return

    return ParsedCallbackQuestionsData(
        answer=_callback_data[0],
        question_id=_callback_data[1]
    )


def format_callback_data_for_question(choice: str, question_id: int) -> str:
    return f'{choice}{_CALLBACK_DATA_DELIMITER}{question_id}'
