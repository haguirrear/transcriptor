import structlog
from fastapi import Request
from gotrue import SyncSupportedStorage

logger = structlog.get_logger(__name__)


class SessionStorage(SyncSupportedStorage):
    def __init__(self, request: Request):
        self.request = request

    def get_item(self, key: str) -> str | None:
        logger.debug(f"Retrieve {key} from session")
        if key in self.request.scope["supabase"]:
            return self.request.scope["supabase"][key]

    def set_item(self, key: str, value: str) -> None:
        logger.debug(f"Saving {key} in session")
        self.request.scope["supabase"][key] = value

    def remove_item(self, key: str) -> None:
        logger.debug(f"Deleting {key} in session")
        if key in self.request.scope["supabase"]:
            del self.request.scope["supabase"][key]
