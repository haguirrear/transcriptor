import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from transcriptor.middleware.cached_static import CacheControl, CachedStatic

from transcriptor.routers import auth, transcriptor
from transcriptor.settings import settings

logging.basicConfig(level=settings.LOG_LEVEL)


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    expose_headers=["HX-Redirect", "HX-Location"],
)


app.mount(
    "/static",
    CachedStatic(
        directory="static",
        cache_control=CacheControl(max_age="2592000", public=True, inmutable=True),
    ),
    name="static",
)

app.include_router(auth.router)
app.include_router(transcriptor.router)
