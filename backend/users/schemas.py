from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: str

class ReadUser(BaseModel):
    id: int
    username: str
    email: str
    registered_at: datetime