from typing import Any

import asyncpg
from pydantic import BaseModel
import asyncio

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
        # TODO: remove get_test_cases
        rows = await self.repo.get_test_cases(coding_question_id=coding_question_id)

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


class ExecutionResult(BaseModel):
    result: Any | None = None
    error: str | None = None


class CodingQuestionsExecutionService:
    def __init__(self, code: str, return_type: str) -> None:
        self.code = self.convert_code(code)
        self.return_type = self.convert_return_type(return_type)

    @staticmethod
    def convert_code(code: str) -> str:
        return code.replace('\"', '').replace('\\n', '\n').replace('\\t', '\t')

    @staticmethod
    def convert_return_type(return_type: str) -> str:
        return f'<class \'{return_type}\'>'

    # TODO: not execute code; it is compilation
    def execute(self) -> ExecutionResult:
        try:
            executable_code = compile(self.code, '<string>', 'exec')
            globals_dict, locals_dict = {}, {}
            exec(executable_code, globals_dict, locals_dict)
        except SyntaxError as e:
            return ExecutionResult(
                error=f'SyntaxError: {e}'
            )
        return ExecutionResult(
            result=locals_dict['solution']
        )

    def validate_input(self) -> str | None:
        if not self.code:
            return 'InputError: input cannot be empty'

        if 'while True:' in self.code:
            return 'ForeverLoopError: function cannot contain forever loop'

    def run_code(self) -> tuple[str, str]:
        # TODO: remove status and result from class attributes

        # TODO: divide func on parts; (def validate_input)
        #
        error = self.validate_input()
        if error:
            return 'error', error

        res = self.execute()

        if res.error:
            return 'error', res.error

        # TODO: refactor (move to execute func)
        try:
            # TODO: un with test cases
            self.result = res.result([1, 2, 3])
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
