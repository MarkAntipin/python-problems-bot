import logging
import time
from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from settings import app_settings

logger = logging.getLogger(app_settings.TITLE)


class LogRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        request_duration = time.perf_counter() - start_time
        logger.info(
            'Request',
            extra={
                'request': {
                    'duration_ms': request_duration * 1000,
                    'path': request.url.path,
                    'method': request.method,
                    'response_status': response.status_code,
                }
            }
        )
        return response
