from datetime import UTC, datetime, timedelta

import asyncpg
from pydantic import BaseModel

from src.models.achievements import Achievement
from src.repositories.postgres.achievements import AchievementsRepo
from src.repositories.postgres.questions import QuestionsRepo


class SolvedQuestion(BaseModel):
    is_correct: bool
    theme: str
    level: int
    created_at: datetime


ACHIEVEMENTS = [
    # special achievements
    Achievement(
        text='Решил по 10 задач разных уровней',
        title='Всесторонний Разум',
        emoji='🧠',
        name='solve_10_different_level_questions',
        emoji_key='brain'
    ),
    Achievement(
        text='Не более 20% ошибок в более чем 50 задачах',
        title='Точный Стрелок',
        emoji='🎯',
        name='less_than_20_percent_errors_in_50_questions',
        emoji_key='target'
    ),
    Achievement(
        text='Вернулся после более чем 3 дней перерыва',
        title='Возвращение Мастера',
        emoji='🥷',
        name='comeback_after_3_days',
        emoji_key='ninja'
    ),
    # correct answers achievements
    Achievement(
        text='Первая правильно решенная задача',
        title='Hello World\\!',
        emoji='🚀',
        name='first_correct_answer',
        emoji_key='rocket'
    ),
    Achievement(
        text='10 правильно решенных задач',
        title='Junior',
        emoji='👶',
        name='solve_10_questions',
        emoji_key='kid'
    ),
    Achievement(
        text='27 правильно решенных задач',
        title='Клуб 27',
        emoji='🎸',
        name='solve_27_questions',
        emoji_key='guitar'
    ),
    Achievement(
        text='50 правильно решенных задач',
        title='Middle',
        emoji='👨‍💻',
        name='solve_50_questions',
        emoji_key='programmer'
    ),
    Achievement(
        text='100 правильно решенных задач',
        title='Senior',
        emoji='👴',
        name='solve_100_questions',
        emoji_key='senior'
    ),
    # correct answers streak achievements
    Achievement(
        text='3 правильных решения подряд',
        title='Хет\\-трик',
        emoji='🏅',
        name='solve_3_questions_in_a_row',
        emoji_key='medal'
    ),
    Achievement(
        text='Решение задач 3 дня подряд',
        title='Марафонец',
        emoji='🏃',
        name='solve_questions_3_days_in_a_row',
        emoji_key='marafon'
    ),
    Achievement(
        text='Решение задач 10 дней подряд',
        title='Серийный решала',
        emoji='🪓',
        name='solve_questions_10_days_in_a_row',
        emoji_key='axe'
    ),
    Achievement(
        text='Решение задач 30 дней подряд',
        title='Iron Man',
        emoji='🦾',
        name='solve_questions_30_days_in_a_row',
        emoji_key='iron'
    ),
    # incorrect answers achievements
    Achievement(
        text='Первая неправильно решенная задача',
        title='Первый блин',
        emoji='🥞',
        name='first_incorrect_answer',
        emoji_key='blin'
    ),
    Achievement(
        text='10 неправильно решенных задач',
        title='Экспериментатор',
        emoji='👨‍🔬',
        name='solve_10_incorrect_questions',
        emoji_key='science'
    ),
    Achievement(
        text='50 неправильно решенных задач',
        title='Король Конфузов',
        emoji='🌚',
        name='solve_50_incorrect_questions',
        emoji_key='moon'
    ),
    # questions on specific topics achievements
    Achievement(
        text='10 решенных задач на тему lists',
        title='Маэстро Массивов',
        emoji='🎼',
        name='solve_10_list_questions',
        emoji_key='music'
    ),
    Achievement(
        text='10 решенных задач на тему loops',
        title='Мастер Циклов',
        emoji='♾️',
        name='solve_10_loops_questions',
        emoji_key='infinity'
    ),
]


class AchievementsService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.questions_repo = QuestionsRepo(pg_pool=pg_pool)
        self.achievements_repo = AchievementsRepo(pg_pool=pg_pool)

    async def get_user_achievements(self, user_id: int) -> list[Achievement]:
        user_achievements = await self.achievements_repo.get_user_achievements_names(user_id=user_id)
        return [achievement for achievement in ACHIEVEMENTS if achievement.name in user_achievements]

    async def check_for_new_achievements(self, user_id: int) -> list[Achievement] | None:
        user_current_achievements = await self.achievements_repo.get_user_achievements_names(user_id=user_id)
        if len(user_current_achievements) == len(ACHIEVEMENTS):
            return

        solved_questions_rows = await self.questions_repo.get_user_solved_questions(user_id=user_id)
        solved_questions = [
            SolvedQuestion(
                is_correct=row['is_correct'],
                theme=row['theme'],
                level=row['level'],
                created_at=row['created_at'],
            ) for row in solved_questions_rows
        ]
        solved_questions.sort(key=lambda x: x.created_at)

        new_achievements = self._check_for_new_achievements(
            solved_questions=solved_questions,
            user_current_achievements=user_current_achievements
        )
        await self.achievements_repo.save_achievements(
            user_id=user_id,
            achievement_names=[achievement.name for achievement in new_achievements]
        )
        return new_achievements

    def _check_for_new_achievements(
            self, solved_questions: list[SolvedQuestion], user_current_achievements: set[str]
    ) -> list[Achievement]:
        new_achievements = []
        for achievement in ACHIEVEMENTS:
            if achievement.name in user_current_achievements:
                continue

            if achievement.name == 'solve_10_different_level_questions':
                if self._solve_10_different_level_questions(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'less_than_20_percent_errors_in_50_questions':
                if self._less_than_20_percent_errors_in_50_questions(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'comeback_after_3_days':
                if self._comeback_after_3_days(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'first_correct_answer':
                if self._first_correct_answer(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_10_questions':
                if self._solve_10_questions(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_27_questions':
                if self._solve_27_questions(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_50_questions':
                if self._solve_50_questions(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_100_questions':
                if self._solve_100_questions(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'first_incorrect_answer':
                if self._first_incorrect_answer(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_10_incorrect_questions':
                if self._solve_10_incorrect_questions(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_50_incorrect_questions':
                if self._solve_50_incorrect_questions(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_10_list_questions':
                if self._solve_10_list_questions(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_10_loops_questions':
                if self._solve_10_loops_questions(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_3_questions_in_a_row':
                if self._solve_3_questions_in_a_row(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_questions_3_days_in_a_row':
                if self._solve_questions_3_days_in_a_row(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_questions_10_days_in_a_row':
                if self._solve_questions_10_days_in_a_row(solved_questions):
                    new_achievements.append(achievement)

            if achievement.name == 'solve_questions_30_days_in_a_row':
                if self._solve_questions_30_days_in_a_row(solved_questions):
                    new_achievements.append(achievement)

        return new_achievements

    @staticmethod
    def _solve_10_different_level_questions(solved_questions: list[SolvedQuestion]) -> bool:
        levels_counter = {}
        for question in solved_questions:
            if question.level not in levels_counter:
                levels_counter[question.level] = 0

            if question.is_correct:
                levels_counter[question.level] += 1

        levels_solved = 0
        for level in levels_counter:
            if levels_counter[level] >= 10:
                levels_solved += 1

        return levels_solved >= 2

    @staticmethod
    def _less_than_20_percent_errors_in_50_questions(solved_questions: list[SolvedQuestion]) -> bool:
        if len(solved_questions) < 50:
            return False

        correct_questions_count = 0
        incorrect_questions_count = 0
        for question in solved_questions:
            if question.is_correct:
                correct_questions_count += 1
            else:
                incorrect_questions_count += 1

        return incorrect_questions_count / (correct_questions_count + incorrect_questions_count) <= 0.2

    @staticmethod
    def _comeback_after_3_days(solved_questions: list[SolvedQuestion]) -> bool:
        if len(solved_questions) < 3:
            return False
        return (solved_questions[-1].created_at - solved_questions[-3].created_at).days >= 3

    @staticmethod
    def __is_soled_questions_match_count(
        solved_questions: list[SolvedQuestion],
        count: int,
        is_correct: bool = True,
        theme: str | None = None,
    ) -> bool:
        questions = solved_questions
        if theme:
            questions = [question for question in solved_questions if question.theme == theme]

        if not questions:
            return False

        correct_questions = [question for question in questions if question.is_correct == is_correct]
        return len(correct_questions) >= count

    def _first_correct_answer(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__is_soled_questions_match_count(solved_questions, 1)

    def _solve_10_questions(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__is_soled_questions_match_count(solved_questions, 10)

    def _solve_27_questions(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__is_soled_questions_match_count(solved_questions, 27)

    def _solve_50_questions(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__is_soled_questions_match_count(solved_questions, 50)

    def _solve_100_questions(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__is_soled_questions_match_count(solved_questions, 100)

    def _first_incorrect_answer(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__is_soled_questions_match_count(solved_questions, 1, is_correct=False)

    def _solve_10_incorrect_questions(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__is_soled_questions_match_count(solved_questions, 10, is_correct=False)

    def _solve_50_incorrect_questions(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__is_soled_questions_match_count(solved_questions, 50, is_correct=False)

    def _solve_10_list_questions(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__is_soled_questions_match_count(solved_questions, 10, theme='lists')

    def _solve_10_loops_questions(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__is_soled_questions_match_count(solved_questions, 10, theme='loops')

    @staticmethod
    def _solve_3_questions_in_a_row(solved_questions: list[SolvedQuestion]) -> bool:
        for i in range(len(solved_questions) - 2):
            if (
                    solved_questions[i].is_correct
                    and solved_questions[i + 1].is_correct
                    and solved_questions[i + 2].is_correct
            ):
                return True
        return False

    @staticmethod
    def __solve_questions_n_days_in_a_row(solved_questions: list[SolvedQuestion], n: int) -> bool:
        today = datetime.now(UTC)
        for i in range(n):
            day_to_check = today - timedelta(days=i)
            if not any(question.created_at.date() == day_to_check.date() for question in solved_questions):
                return False
        return True

    def _solve_questions_3_days_in_a_row(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__solve_questions_n_days_in_a_row(solved_questions, 3)

    def _solve_questions_10_days_in_a_row(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__solve_questions_n_days_in_a_row(solved_questions, 10)

    def _solve_questions_30_days_in_a_row(self, solved_questions: list[SolvedQuestion]) -> bool:
        return self.__solve_questions_n_days_in_a_row(solved_questions, 30)
