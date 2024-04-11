from abc import ABC
from typing import Any, Dict


class SessionRepository(ABC):
    async def get_session(self, session_id: str) -> Dict[str, Any]:
        ...

    async def save_session(self, session_id: str, value: Dict[str, Any]):
        ...
