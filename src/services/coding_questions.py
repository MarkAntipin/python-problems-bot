from typing import Any

import asyncpg
from pydantic import BaseModel

from src.repositories.postgres.coding_questions import CodingQuestionsRepo


class CodingQuestion(BaseModel):
    id: int  # noqa A003
    title: str
    problem: str
    params: str
    return_type: str
    difficulty: str


class TestCase(BaseModel):
    input: Any
    output: Any


class TestCases(BaseModel):
    test_cases: list[TestCase]


class CodingQuestionsService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.repo = CodingQuestionsRepo(pg_pool=pg_pool)

    async def get_coding_question(
            self,
            coding_question_id: int
            # user_id: int
    ) -> tuple[CodingQuestion, TestCases] | None:
        # row = await self.repo.get_decided_coding_question(coding_question_id=coding_question_id, user_id=user_id)
        # if row:
        #     return

        row = await self.repo.get_coding_question_by_id(coding_question_id=coding_question_id)
        if not row:
            return

        coding_question = CodingQuestion(
            id=coding_question_id,
            title=row['title'],
            problem=row['problem'],
            params=row['params'],
            return_type=row['return_type'],
            difficulty=row['difficulty']
        )

        rows = await self.repo.get_test_cases(coding_question_id=coding_question_id)
        print(rows)
        test_cases = []
        for row in rows:
            test_cases.append(TestCase(
                input=row['input'],
                output=row['output']
            ))
        test_cases = TestCases(
            test_cases=test_cases
        )

        return coding_question, test_cases


class CodingQuestionsExecutionService:
    def __init__(self, code: str, return_type: str) -> None:
        self.code = code
        self.return_type = return_type
        self.status = 'error'
        self.result = None

    def convert_code(self) -> None:
        self.code = self.code.replace('\"', '').replace('\\n', '\n').replace('\\t', '\t')

    def convert_return_type(self) -> None:
        self.return_type = f'<class \'{self.return_type}\'>'

    def execute(self) -> tuple[dict, dict] | str:
        try:
            executable_code = compile(self.code, '<string>', 'exec')
            globals_dict, locals_dict = {}, {}
            exec(executable_code, globals_dict, locals_dict)
        except SyntaxError as e:
            return f'SyntaxError: {e}'

        return globals_dict, locals_dict

    def run_code(self) -> tuple[str, str]:
        if not self.code:
            self.result = 'InputError: input cannot be empty'
            return self.status, self.result

        self.convert_code()
        self.convert_return_type()

        if 'while True:' in self.code:
            self.result = 'ForeverLoopError: function cannot contain forever loop'
            return self.status, self.result

        res = self.execute()
        if not isinstance(res, str):
            globals_dict, locals_dict = res
        else:
            self.result = res.replace('<string>, ', '')
            return self.status, self.result

        try:
            self.result = locals_dict['solution']([1, 2, 3])
        except KeyError as e:  # если неправильное имя функции
            self.result = f'FunctionNameError: function name must be {e}'
        except TypeError as e:  # если нет аргументов в определении функции
            self.result = f'FunctionArgsError: {e}'
        except NameError as e:  # если используется переменная, которая не объявлена
            self.result = f'NameError: {e}'
        else:
            if str(type(self.result)) != self.return_type:
                self.status = 'error'
                self.result = f'ReturnTypeError: return type must be {self.return_type}'
            else:
                self.status = 'success'
                self.result = str(self.result)

        return self.status, self.result
