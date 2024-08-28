from fastapi_users.db import SQLAlchemyBaseUserTable

from core.models import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    pass