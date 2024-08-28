from fastapi_users.db import SQLAlchemyBaseUserTable

from core.models import Base
from core.models.mixins.id_int_pk import IdIntPkMixin


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[int]):
    pass