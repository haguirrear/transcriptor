import logging
from typing import Annotated, Literal
from fastapi import APIRouter, Depends, Path, Request
from gotrue import User
from transcriptor.services.auth import CustomSession
from transcriptor.services.payments import create_preference
from transcriptor.dependencies.auth import auth_session, auth_user
from transcriptor.common.templates import templates

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/payments")


@router.get("/billing")
async def billing_settings(
    request: Request,
    session: Annotated[CustomSession, Depends(auth_session)],
    user: Annotated[User, Depends(auth_user)],
):
    return templates.TemplateResponse(
        "billing/index.html",
        {
            "request": request,
            "menu": "billing",
            "email": user.email,
            "full_name": session["name"],
            "picture": session["avatar_url"],
        },
    )


@router.post("/create")
async def create_checkout(
    request: Request, credits: int, user: Annotated[User, Depends(auth_user)]
):
    preference = await create_preference()


@router.get("/{result}")
async def payment_result_callback(
    request: Request,
    result: Annotated[Literal["success", "pending", "failure"], Path()],
    payment_id: str,
    status: Literal["approved", "pending"],
    external_reference: float,
    merchant_order_id: int,
):
    logger.info(request.query_params)
