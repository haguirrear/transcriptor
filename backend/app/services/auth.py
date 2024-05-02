from typing import List, TypedDict
from fastapi import Request
from gotrue.errors import AuthInvalidCredentialsError
from gotrue.types import AuthResponse
from supabase.client import Client


class Profile(TypedDict):
    name: str | None
    last_name: str | None


class CustomSession(TypedDict):
    email: str
    full_name: str | None
    access_token: str
    refresh_token: str


def set_session(
    request: Request, auth_response: AuthResponse, profile: Profile | None = None
):
    if not auth_response.user or not auth_response.session:
        raise Exception("Trying to set empty session")

    request.session.clear()
    request.session["email"] = auth_response.user.email
    if profile:
        request.session["full_name"] = f'{profile["name"]} {profile["last_name"]}'
    request.session["access_token"] = auth_response.session.access_token
    request.session["refresh_token"] = auth_response.session.refresh_token


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
