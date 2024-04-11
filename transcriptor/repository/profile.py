from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from transcriptor.models.profile import ProfileModel


async def get_user_profile(session: AsyncSession, user_id: str):
    query = select(ProfileModel).where(ProfileModel.id == user_id)

    profile = (await session.scalars(query)).first()
    return profile


async def create_user_profile(
    session: AsyncSession,
    user_id: str,
    full_name: str | None = None,
    avatar_url: str | None = None,
):
    profile = ProfileModel(id=user_id, full_name=full_name, avatar_url=avatar_url)
    session.add(profile)
    await session.flush()
    return profile


async def update_user_profile(
    session: AsyncSession,
    user_id: str,
    full_name: str | None = None,
    avatar_url: str | None = None,
):
    profile = await get_user_profile(session, user_id)
    if not profile:
        profile = await create_user_profile(session, user_id, full_name, avatar_url)
        return profile
    if full_name:
        profile.full_name = full_name
    if avatar_url:
        profile.avatar_url = avatar_url

    await session.flush()
    return profile
