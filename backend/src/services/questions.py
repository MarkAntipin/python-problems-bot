import random
from enum import StrEnum, auto

import asyncpg
from pydantic import BaseModel

from settings import bot_settings
from src.mappers.questions import map_question_from_pg_row
from src.models.questions import Question
from src.repositories.postgres.questions import QuestionsRepo
from src.utils.is_answer_correct import is_answer_correct


class GetNewRandomQuestionForUserStatus(StrEnum):
    no_questions_for_today = auto()
    no_more_questions = auto()
    ok = auto()


class GetNewRandomQuestionForUserResp(BaseModel):
    status: GetNewRandomQuestionForUserStatus = GetNewRandomQuestionForUserStatus.ok
    question: Question | None = None


class QuestionsService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.repo = QuestionsRepo(pg_pool=pg_pool)

    async def can_send_question(self, user_id: int) -> bool:
        today_send_questions_count = await self.repo.get_today_answered_questions_count(
            user_id=user_id
        )
        return today_send_questions_count < bot_settings.MAX_QUESTION_PER_DAY

    async def get_new_ordered_question_for_user(self, user_id: int, user_level: int) -> GetNewRandomQuestionForUserResp:
        is_can_send_question = await self.can_send_question(user_id=user_id)
        if not is_can_send_question:
            return GetNewRandomQuestionForUserResp(status=GetNewRandomQuestionForUserStatus.no_questions_for_today)

        row = await self.repo.get_new_ordered_questions_for_user(
            user_id=user_id,
            level=user_level,
        )
        if not row:
            return GetNewRandomQuestionForUserResp(status=GetNewRandomQuestionForUserStatus.no_more_questions)

        return GetNewRandomQuestionForUserResp(
            question=map_question_from_pg_row(row=row),
            status=GetNewRandomQuestionForUserStatus.ok
        )

    async def get_new_random_question_for_user(self, user_id: int, user_level: int) -> GetNewRandomQuestionForUserResp:
        today_send_questions_count = await self.repo.get_today_send_questions_count(
            user_id=user_id
        )
        if today_send_questions_count >= bot_settings.MAX_QUESTION_PER_DAY:
            return GetNewRandomQuestionForUserResp(status=GetNewRandomQuestionForUserStatus.no_questions_for_today)

        rows = await self.repo.get_new_questions_for_user(
            user_id=user_id,
            level=user_level,
            limit=100
        )
        if not rows:
            return GetNewRandomQuestionForUserResp(status=GetNewRandomQuestionForUserStatus.no_more_questions)

        row = random.choice(rows)
        return GetNewRandomQuestionForUserResp(
            question=map_question_from_pg_row(row=row),
            status=GetNewRandomQuestionForUserStatus.ok
        )

    async def get_by_id(self, question_id: int) -> Question | None:
        row = await self.repo.get_by_id(question_id=question_id)
        if not row:
            return
        return map_question_from_pg_row(row=row)

    async def answer_question(
        self,
        user_id: int,
        question: Question,
        user_answer: str
    ) -> bool:
        is_correct = is_answer_correct(user_answer=user_answer, correct_answer=question.answer)
        await self.repo.answer_question(
            question_id=question.id,
            user_id=user_id,
            user_answer=user_answer,
            is_correct=is_correct,
        )
        return is_correct

    async def send_question(
        self,
        user_id: int,
        question_id: int
    ) -> None:
        await self.repo.send_question(
            question_id=question_id,
            user_id=user_id,
        )
