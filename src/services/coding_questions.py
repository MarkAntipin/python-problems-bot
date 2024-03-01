from typing import Any, Callable

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
    input: Any  # noqa:A003
    output: Any


class TestCases(BaseModel):
    test_cases: list[TestCase]


class ReturnTypeError(Exception):
    def __init__(self, return_type: str, wrong_type: str) -> None:
        self.return_type = return_type
        self.wrong_type = wrong_type

    def __str__(self) -> str:
        return f'ReturnTypeError: return type must be {self.return_type}, not {self.wrong_type}'


class WrongOutputError(Exception):
    def __init__(self, correct_output: str, wrong_output: str) -> None:
        self.correct_output = correct_output
        self.wrong_output = wrong_output

    def __str__(self) -> str:
        return f'WrongOutputError: wrong output value {self.wrong_output}, output must be {self.correct_output}'


class CodingQuestionsService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.repo = CodingQuestionsRepo(pg_pool=pg_pool)

    async def get_coding_question(self, coding_question_id: int) -> CodingQuestion | None:
        row = await self.repo.get_coding_question_by_id(coding_question_id=coding_question_id)

        return CodingQuestion(
            id=coding_question_id,
            title=row['title'],
            problem=row['problem'],
            params=row['params'],
            return_type=row['return_type'],
            difficulty=row['difficulty']
        )

    async def get_random_coding_question(self, user_id: int, user_level: int) -> CodingQuestion | None:
        while True:
            row = await self.repo.get_random_coding_question(difficulty=user_level)
            is_decided = await self.repo.get_decided_coding_question(coding_question_id=row['id'], user_id=user_id)
            if not is_decided:
                break

        coding_question = await self.get_coding_question(row['id'])

        return coding_question


class CompilationResult(BaseModel):
    func: Any | None = None
    error: str | None = None


class ExecutionResult(BaseModel):
    result: Any | None = None
    error: str | None = None


class CodingQuestionsExecutionService:
    def __init__(self, pg_pool: asyncpg.Pool, question_id: int, code: str, return_type: str) -> None:
        self.repo = CodingQuestionsRepo(pg_pool=pg_pool)
        self.question_id = question_id
        self.code = self.convert_code(code)
        self.return_type = self.convert_return_type(return_type)

    @staticmethod
    def convert_code(code: str) -> str:
        return code.replace('\"', '').replace('\\n', '\n').replace('\\t', '\t')

    @staticmethod
    def convert_return_type(return_type: str) -> str:
        return f'<class \'{return_type}\'>'

    def compilation(self) -> CompilationResult:
        try:
            executable_code = compile(self.code, '<string>', 'exec')
            globals_dict, locals_dict = {}, {}
            exec(executable_code, globals_dict, locals_dict)
        except SyntaxError as e:
            return CompilationResult(
                error=f'SyntaxError: {e}'
            )
        return CompilationResult(
            func=locals_dict['solution']
        )

    def execute(self, func: Callable, test_case: TestCase) -> ExecutionResult:
        try:
            result = func(test_case.input)

            if str(type(result)) != self.return_type:
                raise ReturnTypeError(return_type=self.return_type, wrong_type=str(type(result)))
            elif result != TestCase.output:
                raise WrongOutputError(
                    correct_output=test_case.output,
                    wrong_output=result
                )
            else:
                return ExecutionResult(
                    result=result
                )
        except KeyError as e:
            error = f'FunctionNameError: function name must be {e}'
        except TypeError as e:
            error = f'FunctionArgsError: {e}'
        except NameError as e:
            error = f'NameError: {e}'
        except ReturnTypeError as e:
            error = str(e)
        except WrongOutputError as e:
            error = str(e)

        return ExecutionResult(
            error=error
        )

    def validate_input(self) -> str | None:
        if not self.code:
            return 'InputError: input cannot be empty'

        if 'while True:' in self.code:
            return 'ForeverLoopError: function cannot contain forever loop'

    async def get_test_cases(self) -> TestCases:
        rows = await self.repo.get_test_cases(coding_question_id=self.question_id)

        test_cases = []
        for row in rows:
            test_cases.append(TestCase(
                input=row['input'],
                output=row['output']
            ))

        return TestCases(
            test_cases=test_cases
        )

    async def run_code(self) -> tuple[str, str]:
        status = 'error'

        error = self.validate_input()
        if error:
            return status, error

        func = self.compilation()
        if func.error:
            return status, func.error

        test_cases = await self.get_test_cases()

        result = None
        for test_case in test_cases.test_cases:
            result = self.execute(func.func, test_case)

        return status, str(result)
