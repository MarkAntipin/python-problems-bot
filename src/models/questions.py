from pydantic import BaseModel


class AnswerRequest(BaseModel):
    user_init_data: str
    question_id: int
    user_answer: str


class AnswerResponse(BaseModel):
    is_correct: bool
