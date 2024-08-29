from fastapi import APIRouter

from .dependencies.router_helper import fastapi_users
from .dependencies.backend import authentication_backend
from .dependencies.schemas import UserRead, UserCreate, UserUpdate


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
    )
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    )
)

# get information about user
# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    )
)
