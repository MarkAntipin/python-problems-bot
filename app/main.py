from typing import Any

from fastapi import FastAPI, Request, Response, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from src.services.coding_questions import CodingQuestionsService


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


class QuestionResult(BaseModel):
    status: str
    data: str


@app.get('/question/{question_id}')
async def get_question_page(request: Request, question_id: int): # noqa ANN201
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "question_id": question_id,
            "params": 'numbers: list[int]',
            "return_type": 'int'
        }
    )


@app.post('/question/{question_id}/result/{return_type}', response_model=QuestionResult)
async def execute_code(question_id: int, return_type: str, code: str = Body()) -> Response:
    coding_questions_service = CodingQuestionsService(code, return_type)
    status, result = coding_questions_service.run_code()

    return JSONResponse(content={
        "status": status,
        "data": result
    })


if __name__ == '__main__':
    uvicorn.run(app)
