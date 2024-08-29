from fastapi import APIRouter

from dependencies.router_helper import fastapi_users
from dependencies.backend import authentication_backend


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_auth_router(authentication_backend),
)
