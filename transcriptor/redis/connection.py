from redis import asyncio as aioredis
from transcriptor.settings import settings


def get_redis_pool():
    if not settings.REDIS_URL:
        return None
    return aioredis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)


pool = get_redis_pool()
