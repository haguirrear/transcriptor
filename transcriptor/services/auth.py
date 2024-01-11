import logging
from typing import List
from typing_extensions import TypedDict
from fastapi import Request
from gotrue import Provider, SignInWithOAuthCredentials
from gotrue.errors import AuthInvalidCredentialsError
from gotrue.types import AuthResponse
from postgrest.base_request_builder import APIResponse
from supabase.client import Client
from transcriptor.settings import settings

logger = logging.getLogger(__name__)


class Profile(TypedDict):
    name: str | None
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
        request.session["name"] = profile["name"]
        request.session["avatar_url"] = profile["avatar_url"]


def login_user(
    request: Request, username: str, password: str, supabase: Client
) -> AuthResponse:
    auth_response = supabase.auth.sign_in_with_password(
        {
            "email": username,
            "password": password,
        }
    )

    if not auth_response.user:
        raise AuthInvalidCredentialsError("Invalid Credentials")

    profiles: List[Profile] = (
        supabase.table("profiles")
        .select("name,last_name")
        .eq("id", auth_response.user.id)
        .execute()
        .data
    )
    profile = None

    if profiles:
        profile = profiles[0]

    set_session(request, auth_response, profile)

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


def login_with_code(request: Request, supabase: Client, code: str):
    auth_response = supabase.auth.exchange_code_for_session({"auth_code": code})  # type: ignore
    if not auth_response.user:
        raise AuthInvalidCredentialsError("Invalid Credentials")

    profiles: APIResponse[Profile] = (
        supabase.table("profiles")
        .upsert(
            {
                "id": auth_response.user.id,
                "name": auth_response.user.user_metadata.get("full_name"),
                "avatar_url": auth_response.user.user_metadata.get("avatar_url"),
            }
        )
        .execute()
    )

    profile = profiles.data[0] if profiles and profiles.data else None

    set_session(request, auth_response, profile)

    return auth_response
