import structlog
from sqlalchemy.ext.asyncio import async_sessionmaker

from .engine import BASE_MAPPER

logger = structlog.get_logger(__name__)


async def get_db():
    AsyncSession = async_sessionmaker(
        # autoflush=True,
        # future=True,
        expire_on_commit=False,
    )
    # Session.configure(binds=BASE_MAPPER)
    logger.debug("CREATING NEW SESSION")
    AsyncSession.configure(binds=BASE_MAPPER)
    session = AsyncSession()

    async with AsyncSession() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
