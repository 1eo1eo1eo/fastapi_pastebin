from typing import Annotated, Sequence

from fastapi import Depends, Path, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .models import Message
from .crud import get_message_by_id, get_message_by_sid


async def message_by_id(
    message_id: Annotated[int, Path],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> Message:
    message = await get_message_by_id(
        message_id=message_id,
        session=session,
    )
    if message is not None:
        return message
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Message {message_id} not found!",
    )


async def message_by_sid(
    message_sid: Annotated[str, Path],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> Sequence[Message]:
    message = await get_message_by_sid(
        message_sid=message_sid,
        session=session,
    )
    if message is not None:
        return message
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Message {message_sid} not found!",
    )
