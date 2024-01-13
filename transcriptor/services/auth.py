import structlog
from fastapi import Request
from gotrue import Provider
from gotrue.errors import AuthInvalidCredentialsError
from gotrue.types import AuthResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import TypedDict

from supabase.client import Client
from transcriptor.repository.profile import get_user_profile, update_user_profile
from transcriptor.settings import settings

logger = structlog.get_logger(__name__)


class Profile(TypedDict):
    full_name: str | None
    avatar_url: str | None


class CustomSession(TypedDict):
    email: str
    name: str | None
    avatar_url: str | None
    access_token: str
    refresh_token: str


def set_session(
    request: Request, auth_response: AuthResponse, profile: Profile | None = None
):
    if not auth_response.user or not auth_response.session:
        raise Exception("Trying to set empty session")

    request.session["email"] = auth_response.user.email
    if profile:
        request.session["name"] = profile["full_name"]
        request.session["avatar_url"] = profile["avatar_url"]


async def login_user(
    db: AsyncSession, request: Request, username: str, password: str, supabase: Client
) -> AuthResponse:
    auth_response = supabase.auth.sign_in_with_password(
        {
            "email": username,
            "password": password,
        }
    )

    if not auth_response.user:
        raise AuthInvalidCredentialsError("Invalid Credentials")

    profile = await get_user_profile(db, auth_response.user.id)
    profile_dict: Profile | None = (
        {"full_name": profile.full_name, "avatar_url": profile.avatar_url}
        if profile
        else None
    )

    set_session(request, auth_response, profile_dict)

    return auth_response


def trigger_oauth_flow(supabase: Client, provider: Provider):
    response = supabase.auth.sign_in_with_oauth(
        {
            "provider": provider,
            "options": {
                "redirect_to": settings.SITE_HOST + "/sso",
                "query_params": {
                    "access_type": "offline",
                    "prompt": "consent",
                },
            },
        }
    )

    return response.url


async def login_with_code(
    db: AsyncSession,
    request: Request,
    supabase: Client,
    code: str,
):
    auth_response = supabase.auth.exchange_code_for_session({"auth_code": code})  # type: ignore
    if not auth_response.user:
        raise AuthInvalidCredentialsError("Invalid Credentials")

    profile = await update_user_profile(
        db,
        auth_response.user.id,
        auth_response.user.user_metadata.get("full_name"),
        auth_response.user.user_metadata.get("avatar_url"),
    )

    set_session(
        request,
        auth_response,
        {"full_name": profile.full_name, "avatar_url": profile.avatar_url},
    )

    return auth_response
