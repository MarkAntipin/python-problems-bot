from fastapi import FastAPI, Request, Response, Body, Query, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import uvicorn

import asyncpg

from src.services.coding_questions import CodingQuestionsService, CodingQuestionsExecutionService
from enum import StrEnum, auto

from settings import PostgresSettings


async def get_pg_pool() -> asyncpg.Pool:
    pg_settings = PostgresSettings()
    return await asyncpg.create_pool(dsn=pg_settings.url)


app = FastAPI(
    title='Mentor Bot'
)

origins = [
    'http://127.0.0.1',
    'http://127.0.0.1:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

templates = Jinja2Templates(directory='templates')


class QuestionData(BaseModel):
    code: str
    return_type: str


class QuestionAnswerStatus(StrEnum):
    success = auto()
    error = auto()


class QuestionResult(BaseModel):
    status: QuestionAnswerStatus
    data: str


# async def get_pg_connection() -> asyncpg.Connection:
#     async with app.state.pool.acquire() as conn:
#         yield conn



@app.on_event('startup')
async def startup() -> None:
    pg_settings = PostgresSettings()
    pool = await asyncpg.create_pool(dsn=pg_settings.url)
    app.state.pool = pool


@app.get('/question/{question_id}')
async def get_question_page(request: Request, question_id: int): # noqa ANN201
    coding_questions_service = CodingQuestionsService(pg_pool=request.app.state.pool)
    coding_question = await coding_questions_service.get_coding_question(coding_question_id=question_id)
    if not coding_question:
        pass

    coding_question, test_cases = coding_question

    return templates.TemplateResponse(
        'main.html',
        {
            'request': request,
            'question_id': question_id,
            'title': coding_question['title'],
            'problem': coding_question['problem'],
            'params': coding_question['params'],
            'return_type': coding_question['return_type']
        }
    )


@app.post('/question/{question_id}/result/', response_model=QuestionResult)
async def execute_code(question_id: int, return_type: str = Query(), code: str = Body()) -> QuestionResult:
    # TODO: get question
    # TODO: get test cases
    # TODO: execute code
    # TODO: check result
    # TODO: save result (return error/success)
    coding_questions_execution_service = CodingQuestionsExecutionService(code, return_type)
    status, result = coding_questions_execution_service.run_code()

    return QuestionResult(
        status=status,
        data=result
    )


if __name__ == '__main__':
    uvicorn.run(app)
