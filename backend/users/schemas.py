from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    username: Annotated[str, MinLen(3), MaxLen(20)]


class UserRead(UserBase):
    id: int
    registered_at: datetime


class UserUpdate(UserCreate):
    pass


class UserUpdatePartial(UserCreate):
    username: str | None = None
    email: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int