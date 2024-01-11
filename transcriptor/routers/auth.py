import logging
from google.oauth2 import id_token
from google.auth.transport import requests
from typing import Annotated
from fastapi import Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.routing import APIRouter
from gotrue import Provider
from gotrue.errors import AuthApiError, AuthInvalidCredentialsError
from supabase.client import Client

from transcriptor.settings import settings

from transcriptor.common.templates import templates
from transcriptor.dependencies.auth import supabase_client
from transcriptor.services.auth import login_with_code, trigger_oauth_flow, login_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/login", name="login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    username: Annotated[str, Form()],
    psw: Annotated[str, Form()],
    supabase: Annotated[Client, Depends(supabase_client)],
):
    try:
        auth_response = login_user(request, username, psw, supabase)
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
    request: Request, supabase: Annotated[Client, Depends(supabase_client)], code: str
):
    try:
        auth_response = login_with_code(request, supabase, code)
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
