from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter
from fastapi import Depends, status

from core.models import db_helper
from .models import Message
from .schemas import MessageCreate, MessageResponse
from .dependencies import message_by_id, message_by_sid
from .crud import create_message
from auth.dependencies.router_helper import current_user, current_superuser
from auth.dependencies.models import User
from auth.dependencies.schemas import UserRead

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("/{message_id}", response_model=MessageResponse)
async def get_user_message(
    message: Annotated[
        Message,
        Depends(message_by_id),
    ],
    user: Annotated[
        User,
        Depends(current_superuser),
    ],
):
    UserRead.model_validate(user)
    return message


@router.get("/{message_sid}", response_model=MessageResponse)
async def get_user_message_by_sid(
    message: Annotated[
        Message,
        Depends(message_by_sid),
    ],
    user: Annotated[
        User,
        Depends(current_user),
    ],
):
    UserRead.model_validate(user)
    return message


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_user_message(
    message_create: MessageCreate,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    user: Annotated[
        User,
        Depends(current_user),
    ],
):
    message = await create_message(
        session=session,
        message_create=message_create,
    )
    UserRead.model_validate(user)
    return message
