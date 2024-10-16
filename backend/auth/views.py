from typing import Annotated, Type
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from fastapi_users import exceptions, schemas
from fastapi_users.router.common import ErrorCode

from auth.dependencies.schemas import UserUpdate
from auth.dependencies.user_manager import get_user_manager
from auth.dependencies.models import User
from core.authentication.user_manager import UserManager
from .dependencies.router_helper import (
    fastapi_users,
    current_user,
)
from auth.dependencies.backend import authentication_backend
from auth.dependencies.schemas import (
    UserRead,
    UserCreate,
    UserUpdate,
)


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
        # requires_verification=True,
    )
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    )
)


# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    )
)


# /request-verify-token
@router.post("/request-verify-token")
async def request_verify_token(
    email: EmailStr,
    user_manager: Annotated[
        UserManager,
        Depends(get_user_manager),
    ],
):
    try:
        user = await user_manager.get_by_email(email)
        await user_manager.request_verify(user)
    except (
        exceptions.UserNotExists,
        exceptions.UserInactive,
        exceptions.UserAlreadyVerified,
    ):
        pass

        return None


# /verify
@router.post("/verify")
async def verify_email(
    request: Request,
    token: str,
    user_manager: Annotated[
        UserManager,
        Depends(get_user_manager),
    ],
    user_schema: Type[schemas.U] = UserRead,
):
    try:
        user = await user_manager.verify(token, request)
        return schemas.model_validate(user_schema, user)
    except (exceptions.InvalidVerifyToken, exceptions.UserNotExists):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
        )
    except exceptions.UserAlreadyVerified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
        )


### how should be verify and require token
# router.include_router(
#     router=fastapi_users.get_verify_router(UserRead),
# )

# /forgot-password
# /reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router(),
)
