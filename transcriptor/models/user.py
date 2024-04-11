from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from transcriptor.models.mixins import DateAuditMixin, UUIDMixin

from .base import Base

if TYPE_CHECKING:
    from .profile import ProfileModel


class UserModel(Base, UUIDMixin, DateAuditMixin):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    email: Mapped[str] = mapped_column(sa.String(30))
    email_confirmed_at: Mapped[datetime | None] = mapped_column()
    invited_at: Mapped[datetime | None] = mapped_column()
    is_super_admin: Mapped[bool | None] = mapped_column(default=False)
    phone: Mapped[str] = mapped_column(sa.Text)
    phone_confirmed_at: Mapped[datetime | None] = mapped_column()
    is_sso_user: Mapped[bool] = mapped_column(server_default="false")
    deleted_at: Mapped[datetime | None] = mapped_column()
    role: Mapped[str | None] = mapped_column()
    raw_app_meta_data: Mapped[Dict[str, Any] | None] = mapped_column()
    raw_user_meta_data: Mapped[Dict[str, Any] | None] = mapped_column()
    last_sign_in_at: Mapped[datetime | None] = mapped_column()

    profile: Mapped[Optional["ProfileModel"]] = relationship(back_populates="user")
