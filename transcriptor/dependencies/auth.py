import logging
from typing import Annotated, NoReturn
from fastapi import Depends, HTTPException, Request
from gotrue.types import User
from supabase.client import Client, ClientOptions
from transcriptor.session.storage import SessionStorage
from transcriptor.services.auth import CustomSession
from transcriptor.settings import settings
from supabase.client import create_client


logger = logging.getLogger(__name__)


def redirect_to_login(request: Request) -> NoReturn:
    login_url = "/login"
    raise HTTPException(
        status_code=307,
        headers={
            "Location": login_url,
            "HX-Redirect": login_url,
        },
    )


def supabase_client(request: Request) -> Client:
    supabase = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_API_KEY,
        ClientOptions(flow_type="pkce", storage=SessionStorage(request)),
    )
    return supabase


async def auth_user(
    request: Request, supabase: Annotated[Client, Depends(supabase_client)]
) -> User:
    user_email = request.session.get("email")

    if not user_email:
        redirect_to_login(request)

    user = supabase.auth.get_user()
    logger.debug(f"Logged user: {user}")
    if not user:
        logger.error("User not available after setting supabase session")
        redirect_to_login(request)
    return user.user


async def auth_session(
    request: Request, supabase: Annotated[Client, Depends(supabase_client)]
) -> CustomSession:
    session: CustomSession = request.session  # type: ignore
    email = session.get("email")

    logger.info(f"Logged user: {email}")
    if not email:
        redirect_to_login(request)

    return session
