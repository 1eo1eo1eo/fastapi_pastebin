import contextlib
import logging

from fastapi_users.exceptions import UserAlreadyExists

from auth.dependencies.schemas import UserCreate
from auth.dependencies.models import User
from auth.dependencies.users import get_users_db
from auth.dependencies.user_manager import get_user_manager
from core.authentication.user_manager import UserManager
from core.models import db_helper
from core.config import settings


log = logging.getLogger(__name__)

get_user_db_context = contextlib.asynccontextmanager(get_users_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(user_manager: UserManager, user_create: UserCreate) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False,
    )

    return user


async def create_superuser(
    email: str = settings.superuser.email,
    password: str = settings.superuser.password,
    is_active: bool = settings.superuser.is_active,
    is_superuser: bool = settings.superuser.is_superuser,
    is_verified: bool = settings.superuser.is_verified,
):
    user_create = UserCreate(
        email=email,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )

    try:
        async with db_helper.session_factory() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                        )
                    )
                    log.warning("User created %r", user)
    except UserAlreadyExists:
        log.warning("User %r already exists", email)
