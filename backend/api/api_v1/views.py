from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter
from fastapi import Depends, status

from fastapi_cache.decorator import cache

from core.models import db_helper
from .models import Message
from .schemas import MessageCreate, MessageResponse
from .dependencies import message_by_id
from .dependencies import message_by_sid
from .crud import create_message, delete_message
from auth.dependencies.router_helper import current_user, current_superuser
from auth.dependencies.models import User
from auth.dependencies.schemas import UserRead

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("/message_by_id/{message_id}", response_model=MessageResponse)
@cache(expire=60)
async def get_user_message(
    user: Annotated[
        User,
        Depends(current_superuser),
    ],
    message: Annotated[
        Message,
        Depends(message_by_id),
    ],
):
    UserRead.model_validate(user)
    return message


@router.get("/message_by_sid/{message_sid}")
@cache(expire=60)
async def get_user_message_by_sid(
    user: Annotated[
        User,
        Depends(current_user),
    ],
    message: Annotated[
        Message,
        Depends(message_by_sid),
    ],
):
    UserRead.model_validate(user)
    return message


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_user_message(
    user: Annotated[
        User,
        Depends(current_user),
    ],
    message_create: MessageCreate,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    message = await create_message(
        session=session,
        message_create=message_create,
    )
    UserRead.model_validate(user)
    return message


@router.delete(
    "/{message_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user_message(
    user: Annotated[
        User,
        Depends(current_superuser),
    ],
    message: Annotated[
        Message,
        Depends(message_by_id),
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    UserRead.model_validate(user)
    return await delete_message(
        message=message,
        session=session,
    )
