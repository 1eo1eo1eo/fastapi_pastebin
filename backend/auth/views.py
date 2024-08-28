from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
)

from .utils import (
    create_access_token,
    get_current_active_auth_user,
    get_current_token_payload,
    validate_auth_user_login,
)
from .schemas import UserSchema, TokenInfo


router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
)


@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: Annotated[
        UserSchema,
        Depends(validate_auth_user_login)
    ]
):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token,
    )


@router.get("/login/me")
def auth_user_check_self_info(
    payload: Annotated[
        dict,
        Depends(get_current_token_payload),
    ],
    user: Annotated[
        UserSchema,
        Depends(get_current_active_auth_user)
    ]
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at:": iat,
    }