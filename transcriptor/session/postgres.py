from typing import Any, Dict

from supabase.client import create_client
from transcriptor.session.base import SessionRepository
from transcriptor.settings import settings


class SupabaseSessionPostgres(SessionRepository):
    def __init__(self) -> None:
        self.supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_API_KEY,
        )

    def get_session(self, session_id: str) -> Dict[str, Any] | None:
        db_resp = (
            self.supabase.table("sessions")
            .select("value")
            .eq("id", session_id)
            .maybe_single()
            .execute()
        )
        if not db_resp or not db_resp.data:
            return None
        return db_resp.data["value"]

    def save_session(self, session_id: str, value: Dict[str, Any]):
        self.supabase.table("sessions").upsert(
            {
                "id": session_id,
                "value": value,
            }
        ).execute()
