from datetime import timedelta
from typing import Any, Dict

import orjson
from redis.asyncio import ConnectionPool, Redis

from transcriptor.session.base import SessionRepository
from transcriptor.settings import settings


class SupabaseSessionRedis(SessionRepository):
    def __init__(self, pool: ConnectionPool) -> None:
        self.redis: Redis = Redis.from_pool(pool)

    async def get_session(self, session_id: str) -> Dict[str, Any] | None:
        resp = await self.redis.get(f"sessions:{session_id}")  # type:ignore
        if not resp:
            return None

        # Renew expiration
        self.redis.pexpire(
            f"sessions:{session_id}", timedelta(days=settings.SESSION_DURATION_DAYS)
        )
        return orjson.loads(resp)

    async def save_session(self, session_id: str, value: Dict[str, Any]):
        await self.redis.setex(
            f"sessions:{session_id}",
            timedelta(days=settings.SESSION_DURATION_DAYS),
            orjson.dumps(value).decode("utf-8"),
        )  # type:ignore
