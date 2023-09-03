import json

import asyncpg
from pydantic import BaseModel

from src.repositories.postgres.onboarding_questions import OnboardingQuestionsRepo
from src.utils.is_answer_correct import is_answer_correct


class OnboardingQuestion(BaseModel):
    id: int  # noqa A003
    text: str
    answer: str
    choices: dict


class OnboardingQuestionsService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.repo = OnboardingQuestionsRepo(pg_pool=pg_pool)

    async def get_new_question_for_user(self, user_id: int) -> OnboardingQuestion | None:
        row = await self.repo.get_new_question_for_user(user_id=user_id)
        if not row:
            return
        return OnboardingQuestion(
            id=row['id'],
            text=row['text'],
            answer=row['answer'],
            choices=json.loads(row['choices']),
        )

    async def _get_by_id(self, question_id: int) -> OnboardingQuestion | None:
        row = await self.repo.get_by_id(question_id=question_id)
        if not row:
            return
        return OnboardingQuestion(
            id=row['id'],
            text=row['text'],
            answer=row['answer'],
            choices=json.loads(row['choices']),
        )

    async def answer_question(
        self,
        user_id: int,
        question_id: int,
        user_answer: str
    ) -> tuple[OnboardingQuestion | None, bool | None]:
        onboarding_question: OnboardingQuestion = await self._get_by_id(
            question_id=question_id
        )
        if not onboarding_question:
            return

        is_correct = is_answer_correct(user_answer=user_answer, correct_answer=onboarding_question.answer)
        await self.repo.answer_question(
            question_id=onboarding_question.id,
            user_id=user_id,
            user_answer=user_answer,
            is_correct=is_correct,
        )
        return onboarding_question, is_correct
