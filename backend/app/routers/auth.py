import logging
from typing import Annotated

from fastapi import Depends, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from gotrue.errors import AuthApiError, AuthInvalidCredentialsError

from backend.app.components import catalog
from backend.app.dependencies.auth import supabase_client
from backend.app.services.auth import login_user
from supabase.client import Client

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/login", name="login", response_class=HTMLResponse)
async def login(request: Request):
    # return templates.TemplateResponse("login/login.html", {"request": request})
    return catalog.render("Login")


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
        return catalog.render("Login.Form", error=e.message)
        # return templates.TemplateResponse(
        #     "login/login-form.html", {"request": request, "error": e.message}
        # )

    auth_response.user
    response = Response(status_code=204)
    response.headers["HX-Location"] = "/app"
    return response


@router.post("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    login_url = "/login"
    return Response(
        status_code=204, headers={"HX-Redirect": login_url, "Location": login_url}
    )
