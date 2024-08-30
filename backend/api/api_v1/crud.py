from typing import Annotated, TYPE_CHECKING, Sequence

from sqlalchemy import select

from .schemas import MessageCreate
from .models import Message

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_message_by_id(
    session: "AsyncSession",
    message_id: int,
) -> Message | None:
    return await session.get(Message, message_id)


async def get_message_by_sid(
    session: "AsyncSession",
    message_sid: str,
) -> Sequence[Message] | None:
    stmt = select(Message).where(Message.sid == message_sid)
    result = await session.scalars(stmt)
    return result.all()


async def create_message(
    session: "AsyncSession",
    message_create: MessageCreate,
) -> Message:
    message = Message(**message_create.model_dump())
    session.add(message)
    await session.commit()
    return message


async def delete_message(
    session: "AsyncSession",
    message: Message,
) -> None:
    await session.delete(message)
    await session.commit()
