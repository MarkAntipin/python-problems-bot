import json
import random
from enum import StrEnum, auto

import asyncpg
from pydantic import BaseModel

from settings import MAX_CODING_QUESTION_PER_DAY
from src.repositories.postgres.coding_questions import CodingQuestionsRepo
from src.utils.is_answer_correct import is_answer_correct


class CodingQuestion(BaseModel):
    id: int  # noqa A003
    title: str
    text: str
    def_init: str
    difficulty: dict


class CodingQuestionsService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.repo = CodingQuestionsRepo(pg_pool=pg_pool)

    async def is_answered_all_questions_for_today(self, user_id: int) -> bool:
        today_answered_coding_questions_count = await self.repo.get_today_answered_coding_questions_count(
            user_id=user_id
        )
        if today_answered_coding_questions_count >= MAX_CODING_QUESTION_PER_DAY:
            return True
        return False

    async def get_new_random_question_for_user(self, user_id: int, user_level: int) -> GetNewRandomCodingQuestionForUserResp:
        today_send_questions_count = await self.repo.get_today_send_coding_questions_count(
            user_id=user_id
        )
        if today_send_questions_count >= MAX_CODING_QUESTION_PER_DAY:
            return GetNewRandomCodingQuestionForUserResp(
                status=GetNewRandomCodingQuestionForUserStatus.no_coding_questions_for_today
            )

        rows = await self.repo.get_new_questions_for_user(
            user_id=user_id,
            level=user_level,
            limit=10
        )
        if not rows:
            return GetNewRandomCodingQuestionForUserResp(
                status=GetNewRandomCodingQuestionForUserStatus.no_more_coding_questions
            )

        row = random.choice(rows)
        return GetNewRandomCodingQuestionForUserResp(
            question=CodingQuestion(
                id=row['id'],
                text=row['text'],
                answer=row['answer'],
                explanation=row['explanation'],
                choices=json.loads(row['choices']),
            ),
            status=GetNewRandomCodingQuestionForUserStatus.ok
        )

    async def get_by_id(self, coding_question_id: int) -> CodingQuestion | None:
        row = await self.repo.get_by_id(coding_question_id=coding_question_id)
        if not row:
            return
        return CodingQuestion(
            id=row['id'],
            text=row['text'],
            answer=row['answer'],
            explanation=row['explanation'],
            choices=json.loads(row['choices']),
        )

    async def answer_question(self, user_id: int, coding_question: CodingQuestion, user_answer: str) -> bool:
        is_correct = is_answer_correct(user_answer=user_answer, correct_answer=coding_question.answer)
        await self.repo.answer_question(
            id=coding_question.id,
            title=title,
            text=text,
            def_inti=def_inti,
        )
        return is_correct

    async def send_question(self, user_id: int, coding_question_id: int) -> None:
        await self.repo.send_coding_question(
            coding_question_id=coding_question_id,
            user_id=user_id,
        )
