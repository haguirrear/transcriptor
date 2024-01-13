import uuid

import structlog
from starlette.datastructures import URL
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from transcriptor.session.base import SessionRepository

logger = structlog.get_logger(__name__)


class SupabaseSessionMiddleware:
    def __init__(self, app: ASGIApp, storage: SessionRepository) -> None:
        self.app = app
        self.storage = storage

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        url = URL(scope=scope)
        if "/static" in url.path:
            return await self.app(scope, receive, send)

        supabase_session_id: str | None = scope["session"].get("supabase_session_id")
        scope["supabase"] = {}
        if supabase_session_id:
            db_resp = self.storage.get_session(supabase_session_id)
            logger.debug(f"Obtaining session {supabase_session_id}: {db_resp}")
            if db_resp:
                scope["supabase"] = db_resp
        else:
            supabase_session_id = str(uuid.uuid4())
            scope["session"]["supabase_session_id"] = supabase_session_id

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                supabase_value = scope.get("supabase")
                if supabase_value:
                    logger.debug(
                        f"Writting session {supabase_session_id}: {supabase_value}"
                    )
                    self.storage.save_session(supabase_session_id, supabase_value)

            await send(message)

        await self.app(scope, receive, send_wrapper)
