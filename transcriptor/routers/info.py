from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from transcriptor.common.templates import templates

router = APIRouter()


@router.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request):
    return templates.TemplateResponse("privacy.html", {"request": request})
