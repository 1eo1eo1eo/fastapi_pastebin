from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    model_config = ConfigDict(strict=True)

    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: str


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