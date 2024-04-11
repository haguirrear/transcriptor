from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import transcriptor.common.logging
from transcriptor.db.engine import dispose_engine, init_engine
from transcriptor.middleware.rate_limit import RateLimitMiddleware
from transcriptor.middleware.supabase_session import SupabaseSessionMiddleware
from transcriptor.redis.connection import pool
from transcriptor.routers import auth, info, payments, transcriptor
from transcriptor.session.redis import SupabaseSessionRedis
from transcriptor.settings import settings

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Startup")
    await init_engine()
    yield
    # Shutdown
    await dispose_engine()


app = FastAPI(lifespan=lifespan, openapi_url=None, docs_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    expose_headers=["HX-Redirect", "HX-Location"],
)
app.add_middleware(SupabaseSessionMiddleware, storage=SupabaseSessionRedis(pool))
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(RateLimitMiddleware, pool=pool)


app.mount("/static", StaticFiles(directory="transcriptor/static"), name="static")

app.include_router(auth.router)
app.include_router(transcriptor.router)
app.include_router(info.router)
app.include_router(payments.router)
