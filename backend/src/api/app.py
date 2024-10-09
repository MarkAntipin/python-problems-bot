import asyncpg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from telegram.ext import Application

from settings import IMAGES_DIR, AppSettings, PostgresSettings, bot_settings
from src.api.middlewares.exception import LogExceptionMiddleware
from src.api.middlewares.logging import LogRequestsMiddleware
from src.api.routers.v1.payment import router as payment_router_v1
from src.api.routers.v1.questions import router as questions_router_v1
from src.api.routers.v1.users import router as users_router_v1
from src.utils.logging.logger import init_logger


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


def setup_bot(app: FastAPI) -> None:
    bot = Application.builder().token(bot_settings.TOKEN).build().bot
    app.state.bot = bot


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
        setup_bot(app)

    @app.on_event('shutdown')
    async def shutdown() -> None:
        await app.state.pg_pool.close()

    app.include_router(questions_router_v1)
    app.include_router(users_router_v1)
    app.include_router(payment_router_v1)

    app.mount('/api/images', StaticFiles(directory=IMAGES_DIR))
    return app
