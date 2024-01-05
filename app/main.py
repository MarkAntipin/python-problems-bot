from fastapi import FastAPI, Request, Body
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
import uvicorn

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


@app.get('/question/{question_id:int}')
async def get_question_page(request: Request, question_id: int): # noqa ANN201
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "question_id": question_id,
        }
    )


@app.post('/question/{question_id:int}/result')
async def execute_code(body: str = Body()):
    compiled_code = compile(body, __name__, 'exec')
    print(exec(compiled_code))

    return {
        "status": "success",
        "data": 'result'
    }


if __name__ == '__main__':
    uvicorn.run(app)
