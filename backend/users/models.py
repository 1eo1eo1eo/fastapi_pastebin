from datetime import datetime
from sqlalchemy import TIMESTAMP
from core.models import Base

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped


class User(Base):
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[TIMESTAMP] = mapped_column(type_=TIMESTAMP, default=datetime.now)