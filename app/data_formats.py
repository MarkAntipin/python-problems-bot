from pydantic import BaseModel
from enum import StrEnum, auto


class QuestionData(BaseModel):
    code: str
    return_type: str


class QuestionAnswerStatus(StrEnum):
    success = auto()
    error = auto()


class QuestionResult(BaseModel):
    status: QuestionAnswerStatus
    data: str
