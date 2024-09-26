from pydantic import BaseModel

from src.models.users import UserInitDataRaw


class AnswerRequest(UserInitDataRaw):
    question_id: int
    user_answer: str


class AnswerResponse(BaseModel):
    is_correct: bool
