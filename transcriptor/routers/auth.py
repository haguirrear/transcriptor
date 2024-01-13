from typing import Annotated

import structlog
from fastapi import Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from gotrue import Provider
from gotrue.errors import AuthApiError, AuthInvalidCredentialsError
from sqlalchemy.ext.asyncio import AsyncSession

from supabase.client import Client
from transcriptor.common.templates import templates
from transcriptor.db.session import get_db
from transcriptor.dependencies.auth import supabase_client
from transcriptor.services.auth import login_user, login_with_code, trigger_oauth_flow

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.get("/login", name="login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    username: Annotated[str, Form()],
    psw: Annotated[str, Form()],
    supabase: Annotated[Client, Depends(supabase_client)],
):
    try:
        auth_response = await login_user(db, request, username, psw, supabase)
    except (AuthInvalidCredentialsError, AuthApiError) as e:
        return templates.TemplateResponse(
            "login/login-form.html", {"request": request, "error": e.message}
        )

    else:
        auth_response.user
        response = Response(status_code=204)
        response.headers["HX-Location"] = "/"
        return response


@router.get("/sso/{provider}")
async def oauth_trigger(
    provider: Provider, supabase: Annotated[Client, Depends(supabase_client)]
):
    url = trigger_oauth_flow(supabase, provider)
    return RedirectResponse(url, status_code=302)


@router.get("/sso")
async def login_with_sso(
    request: Request,
    supabase: Annotated[Client, Depends(supabase_client)],
    db: Annotated[AsyncSession, Depends(get_db)],
    code: str,
):
    try:
        await login_with_code(db, request, supabase, code)
    except (AuthInvalidCredentialsError, AuthApiError) as e:
        return templates.TemplateResponse(
            "login/login.html", {"request": request, "error": e.message}
        )

    return RedirectResponse("/")


@router.post("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    login_url = "/login"
    return Response(
        status_code=204, headers={"HX-Redirect": login_url, "Location": login_url}
    )
