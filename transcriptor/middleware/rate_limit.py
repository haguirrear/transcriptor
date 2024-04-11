from datetime import datetime, timedelta

import structlog
from fastapi import Request, Response
from redis.asyncio import ConnectionPool, Redis
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from transcriptor.settings import settings

logger = structlog.get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, pool: ConnectionPool) -> None:
        super().__init__(app, None)
        self.redis = Redis.from_pool(pool)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        ip = request.client.host if request.client else "0.0.0.0"
        key = f"ip:{ip}:{datetime.now().minute}"

        count = await self.redis.incrby(key, 1)
        logger.debug(f"Ip: {ip} has made {count} request in the current minute")
        await self.redis.expire(key, timedelta(minutes=1))

        if int(count) > settings.MAX_REQUEST_PER_MINUTE:
            return Response(
                status_code=403,
                content="Forbidden: Too many requests",
                media_type="text/html",
            )
        response = await call_next(request)
        return response
