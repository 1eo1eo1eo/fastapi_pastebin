from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from auth.dependencies.models import User
from auth.dependencies.router_helper import current_user, current_superuser
from auth.dependencies.schemas import UserRead


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("")
def get_user_messages(
    user: Annotated[
        User,
        Depends(current_user),
    ],
):
    return {
        "messages": ["m1", "m2", "m3"],
        "user": UserRead.model_validate(user),
    }


@router.get("/secrets")
def get_superuser_messages(
    user: Annotated[
        User,
        Depends(current_superuser),
    ],
):
    return {
        "messages": ["secret-m1", "secret-m2", "secret-m3"],
        "user": UserRead.model_validate(user),
    }
