
import asyncpg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import AppSettings, PostgresSettings
from src.api.routers.v1.questions import router as questions_router_v1
from src.api.routers.v1.users import router as users_router_v1

from ..utils.logging.logger import init_logger
from .middlewares.exception import LogExceptionMiddleware
from .middlewares.logging import LogRequestsMiddleware


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        LogExceptionMiddleware,
    )
    app.add_middleware(
        LogRequestsMiddleware,
    )


async def setup_pg_pool(app: FastAPI) -> None:
    pg_settings = PostgresSettings()
    pg_pool = await asyncpg.create_pool(dsn=pg_settings.url)
    app.state.pg_pool = pg_pool


def create_app(settings: AppSettings) -> FastAPI:
    init_logger(name=settings.TITLE, is_debug=settings.IS_DEBUG)
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
    )
    setup_middlewares(app)

    @app.on_event('startup')
    async def startup() -> None:
        await setup_pg_pool(app)

    @app.on_event('shutdown')
    async def shutdown() -> None:
        await app.state.pg_pool.close()

    app.include_router(questions_router_v1)
    app.include_router(users_router_v1)
    return app
