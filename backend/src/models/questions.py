from pydantic import BaseModel

from src.models.achievements import Achievement
from src.models.users import UserInitDataRaw


class AnswerRequest(UserInitDataRaw):
    question_id: int
    user_answer: str


class AnswerResponse(BaseModel):
    is_correct: bool
    achievements: list[Achievement] | None = None


class Question(BaseModel):
    id: int  # noqa A003
    text: str
    answer: str
    choices: dict
    explanation: str | None
    from_interview: bool = False,
    code_block: str | None = None
    question_text: str | None = None
