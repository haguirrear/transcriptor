import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi.responses import HTMLResponse

from backend.app.components import catalog
from backend.app.dependencies.auth import auth_session
from backend.app.errors import ControlledException
from backend.app.services.auth import CustomSession
from backend.app.services.transcriptor import generate_transcription

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/app", name="index", response_class=HTMLResponse)
async def index(
    request: Request, session: Annotated[CustomSession, Depends(auth_session)]
):
    # return templates.TemplateResponse(
    #     "transcriptor/index.html",
    #     {
    #         "request": request,
    #         "email": session["email"],
    #         "full_name": session.get("full_name"),
    #     },
    # )
    return catalog.render(
        "Transcriptor", email=session["email"], full_name=session.get("full_name")
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
        # return templates.TemplateResponse(
        #     "transcriptor/file-uploader.html", {"request": request, "error": e.message}
        # )
        return catalog.render("Transcriptor.FileUploader", error=e.message)

    # return templates.TemplateResponse(
    #     "transcriptor/transcription.html", {"request": request, "transcription": trans}
    # )
    return catalog.render("Transcriptor.FileUploader", transcription=trans)
