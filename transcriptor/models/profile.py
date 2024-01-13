import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from transcriptor.models.base import Base
from transcriptor.models.mixins import DateAuditMixin, IntegerIDMixin
from transcriptor.models.user import UserModel


class ProfileModel(Base, IntegerIDMixin, DateAuditMixin):
    __tablename__ = "profiles"

    __table_args__ = {"schema": "public"}

    full_name: Mapped[str | None] = mapped_column()
    avatar_url: Mapped[str | None] = mapped_column()
    user_id: Mapped[uuid.UUID] = mapped_column(sa.ForeignKey("auth.users.id"))
    user: Mapped[UserModel] = relationship()
