import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from transcriptor.models.base import Base
from transcriptor.models.mixins import DateAuditMixin
from transcriptor.models.user import UserModel


class ProfileModel(Base, DateAuditMixin):
    __tablename__ = "profiles"

    __table_args__ = {"schema": "public"}

    id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey("auth.users.id"), primary_key=True
    )
    full_name: Mapped[str | None] = mapped_column()
    avatar_url: Mapped[str | None] = mapped_column()
    user: Mapped[UserModel] = relationship(back_populates="profile")
