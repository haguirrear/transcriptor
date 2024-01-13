from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .annotations import int_pk, uuid_pk


class IntegerIDMixin:
    id: Mapped[int_pk]


class UUIDMixin:
    id: Mapped[uuid_pk]


class IsActiveMixin:
    is_active: Mapped[bool] = mapped_column(default=True)


class DateAuditMixin:
    created_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True),
        onupdate=sa.func.now(),
    )
