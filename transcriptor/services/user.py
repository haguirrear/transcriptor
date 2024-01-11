from supabase.client import Client


async def update_openai_key(supabase_client: Client, user_id: str, openai_key: str):
    resp = (
        supabase_client.table("profile")
        .select("openai_key")
        .eq("id", user_id)
        .execute()
    )
