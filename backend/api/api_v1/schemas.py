from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict

from auth.dependencies.router_helper import current_user


class MessageBase(BaseModel):
    title: str
    content: str
    language: str


class MessageRead(MessageBase):
    id: int
    created_at: datetime


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    pass


class MessageResponse(MessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
