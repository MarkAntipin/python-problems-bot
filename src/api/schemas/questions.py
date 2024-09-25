from pydantic import BaseModel


class AnswerRequest(BaseModel):
    user_id: int
    question_id: int
    user_answer: str


class AnswerResponse(BaseModel):
    is_correct: bool


class IsAnsweredAllResponse(BaseModel):
    is_answered_all: bool
