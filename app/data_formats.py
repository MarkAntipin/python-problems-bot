from enum import StrEnum, auto

from pydantic import BaseModel


class QuestionData(BaseModel):
    code: str
    return_type: str


class QuestionAnswerStatus(StrEnum):
    success = auto()
    error = auto()


class QuestionResult(BaseModel):
    status: QuestionAnswerStatus
    data: str
