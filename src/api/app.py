import logging

import asyncpg
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from settings import AppSettings, PostgresSettings
from src.api.routers.v1.questions import router as questions_router_v1
from src.api.routers.v1.users import router as users_router_v1

logger = logging.getLogger(__name__)


class LogExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            logger.warning(f"HTTPException occurred: {http_exc.detail}, (Path: {request.url.path})")
            raise http_exc
        except Exception:
            logger.exception("Unhandled exception occurred. Path: {request.url.path}, Method: {request.method}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )


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


async def setup_pg_pool(app: FastAPI) -> None:
    pg_settings = PostgresSettings()
    pg_pool = await asyncpg.create_pool(dsn=pg_settings.url)
    app.state.pg_pool = pg_pool


def create_app(settings: AppSettings) -> FastAPI:
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
