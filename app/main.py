from contextlib import asynccontextmanager

import asyncpg
import uvicorn
from data_formats import QuestionResult
from fastapi import Body, FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from settings import WEB_APP_URL, PostgresSettings
from src.services.coding_questions import CodingQuestionsExecutionService, CodingQuestionsService


async def get_pg_pool() -> asyncpg.Pool:
    pg_settings = PostgresSettings()
    return await asyncpg.create_pool(dsn=pg_settings.url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    pg_settings = PostgresSettings()
    pool = await asyncpg.create_pool(dsn=pg_settings.url)
    app.state.pool = pool
    yield


app = FastAPI(
    title='Mentor Bot',
    lifespan=lifespan
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
# app.add_middleware(
#     HTTPSRedirectMiddleware
# )

templates = Jinja2Templates(directory='templates')


@app.get('/question/{question_id}')
async def get_question_page(request: Request, question_id: int): # noqa ANN201
    coding_questions_service = CodingQuestionsService(pg_pool=request.app.state.pool)
    coding_question = await coding_questions_service.get_coding_question(coding_question_id=question_id)
    if not coding_question:
        return templates.TemplateResponse(
            'error.html',
            {
                'question': coding_question.title
            }
        )

    url = WEB_APP_URL.format(question_id=question_id, return_type=coding_question.return_type)

    return templates.TemplateResponse(
        'main.html',
        {
            'request': request,
            'url': url,
            'question_id': question_id,
            'title': coding_question.title,
            'problem': coding_question.problem,
            'params': coding_question.params,
            'return_type': coding_question.return_type
        }
    )


@app.post('/question/{question_id}/result/', response_model=QuestionResult)
async def execute_code(request: Request, question_id: int, return_type: str = Query(), code: str = Body()):
    # TODO: get question
    # TODO: get test cases
    # TODO: execute code
    # TODO: check result
    # TODO: save result (return error/success)
    coding_questions_execution_service = CodingQuestionsExecutionService(
        pg_pool=request.app.state.pool,
        question_id=question_id,
        code=code,
        return_type=return_type
    )
    status, result = coding_questions_execution_service.run_code()

    return QuestionResult(
        status=status,
        data=result
    )


if __name__ == '__main__':
    uvicorn.run(app)
