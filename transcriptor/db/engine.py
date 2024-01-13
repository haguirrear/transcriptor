from typing import Dict

import structlog
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from transcriptor.models.base import Base
from transcriptor.settings import settings

logger = structlog.get_logger(__name__)

BASE_MAPPER: Dict[DeclarativeBase, AsyncEngine | None] = {}


async def init_engine():
    engine_options = {
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "echo": True,
    }

    # Add all databases connections here if multible db present
    logger.debug(f"Connecting to database: {settings.DATABASE_URL}")
    BASE_MAPPER[Base] = create_async_engine(settings.DATABASE_URL, **engine_options)
    logger.debug("DB Connected")


async def dispose_engine():
    for engine in BASE_MAPPER.values():
        if engine is not None:
            await engine.dispose()
