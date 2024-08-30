from datetime import datetime, timezone
from sqlalchemy import ForeignKey, TIMESTAMP, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from core.models import Base
from core.models.mixins import IdIntPkMixin


class Message(IdIntPkMixin, Base):
    title: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(nullable=False)
    language: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        type_=TIMESTAMP,
        default=datetime.now(timezone.utc),
    )
    sid: Mapped[str] = mapped_column(ForeignKey("users.id"))
