import secrets
from datetime import datetime, timezone
from sqlalchemy import String, DateTime
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
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
    )
    sid: Mapped[str] = mapped_column(
        nullable=False,
        default=secrets.token_hex,
        unique=True,
    )
