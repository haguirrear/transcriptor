from typing import Annotated

import structlog
from fastapi import APIRouter, Depends, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from gotrue import User

from transcriptor.common.templates import templates
from transcriptor.dependencies.auth import auth_session, auth_user
from transcriptor.errors import ControlledException
from transcriptor.services.auth import CustomSession
from transcriptor.services.transcriptor import generate_transcription

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/", name="index", response_class=HTMLResponse)
async def index(
    request: Request,
    session: Annotated[CustomSession, Depends(auth_session)],
    user: Annotated[User, Depends(auth_user)],
):
    return templates.TemplateResponse(
        "transcriptor/index.html",
        {
            "request": request,
            "email": user.email,
            "full_name": session["name"],
            "picture": session["avatar_url"],
            "menu": "transcribe",
        },
    )


@router.post("/upload", response_class=HTMLResponse)
async def upload_audio(
    request: Request,
    file: UploadFile,
    session: Annotated[CustomSession, Depends(auth_session)],
):
    try:
        trans = await generate_transcription(file)
    except ControlledException as e:
        return templates.TemplateResponse(
            "transcriptor/file-uploader.html", {"request": request, "error": e.message}
        )

    return templates.TemplateResponse(
        "transcriptor/transcription.html", {"request": request, "transcription": trans}
    )


@router.post("/openai")
async def save_openai_key(request: Request, api_key: Annotated[str, Form]):
    pass
