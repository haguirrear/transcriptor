import logging
from typing import Annotated, NoReturn
from fastapi import Depends, HTTPException, Request
from gotrue.types import User
from supabase.client import Client
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


def supabase_client() -> Client:
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_API_KEY)
    return supabase


def auth_supabase_client(
    request: Request, supabase: Annotated[Client, Depends(supabase_client)]
) -> Client:
    access_token = request.session.get("access_token")
    refresh_token = request.session.get("refresh_token")
    if not access_token or not refresh_token:
        logger.info("Access token or refresh token not present in session")
        redirect_to_login(request)

    try:
        supabase.auth.set_session(access_token, refresh_token)
    except Exception as e:
        logger.info(f"Session Invalid or expired: {e}")
        redirect_to_login(request)

    return supabase


async def auth_user(
    request: Request, supabase: Annotated[Client, Depends(auth_supabase_client)]
) -> User:
    user_id = request.session.get("user_id")

    logger.info(f"Logged user id: {user_id}")
    if not user_id:
        redirect_to_login(request)

    user = supabase.auth.get_user()
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
