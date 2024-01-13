from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import transcriptor.logging
from transcriptor.db.engine import dispose_engine, init_engine
from transcriptor.middleware.supabase_session import SupabaseSessionMiddleware
from transcriptor.routers import auth, info, payments, transcriptor
from transcriptor.session.postgres import SupabaseSessionPostgres
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
app.add_middleware(SupabaseSessionMiddleware, storage=SupabaseSessionPostgres())
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(transcriptor.router)
app.include_router(info.router)
app.include_router(payments.router)
