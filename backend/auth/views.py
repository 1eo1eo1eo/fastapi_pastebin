from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from .dependencies.router_helper import fastapi_users
from .dependencies.backend import authentication_backend
from .dependencies.schemas import UserRead, UserCreate, UserUpdate


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    dependencies=[Depends(http_bearer)],
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
