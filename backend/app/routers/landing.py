import logging

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from backend.app.components import catalog

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", name="landing", response_class=HTMLResponse)
async def landing(request: Request):
    return catalog.render("Landing")
