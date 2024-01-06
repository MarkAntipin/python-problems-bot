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
async def execute_code(code: str = Body()):
    code = code.replace('\"', '').split('\\n')
    func_def, func_body = code[0], code[1:]
    code = f'''{func_def}'''

    for i in func_body:
        code += f'\n{i}'

    # if 'while True:' in code:
    #     return {
    #         "status": "error",
    #         "data": "ForeverLoopError: function cannot contain while True"
    #     }

    executable_code = compile(code, '<string>', 'exec')
    globals_dict, locals_dict = {}, {}
    exec(executable_code, globals_dict, locals_dict)

    try:
        result = locals_dict['func'](10, 5)
        print(2)
    except KeyError as e:  # если неправильное имя функции
        result = f'FunctionNameError: function name must be {e}'
        status = 'error'
    except TypeError:  # если нет аргументов в определении функции
        args_num = 2
        result = f'FunctionArgsError: function must take {args_num} positional arguments'
        status = 'error'
    except NameError as e:  # если используется переменная, которая не объявлена
        result = f'NameError: {e}'
        status = 'error'
    else:
        status = 'success'

    return {
        "status": status,
        "data": result
    }


if __name__ == '__main__':
    uvicorn.run(app)
