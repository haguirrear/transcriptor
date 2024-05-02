import logging

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import FileResponse, RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend.app.middleware.cached_static import CacheControl, CachedStatic
from backend.app.middleware.not_found import NotFoundRedirectMiddleware
from backend.app.routers import auth, landing, transcriptor
from backend.app.settings import settings

logging.basicConfig(level=settings.LOG_LEVEL)


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    expose_headers=["HX-Redirect", "HX-Location"],
)
app.add_middleware(NotFoundRedirectMiddleware)


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
app.include_router(landing.router)


@app.get("/health")
async def health():
    return {"health": "ok"}


@app.get("/favicon.ico")
async def favicon(response: Response):
    response.headers["Cache-Control"] = "public, max-age=31536000"
    return FileResponse("static/svg/revol.svg")


@app.get("/404")
async def NotFound(response: Response):
    response.headers["Cache-Control"] = "public, max-age=31536000"
    return FileResponse("static/NotFound.html", media_type="text/html")


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return RedirectResponse(url="/404")
    else:
        return await http_exception_handler(request, exc)
