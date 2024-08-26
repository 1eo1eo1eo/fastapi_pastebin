from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from users.schemas import CreateUser
from users.models import User


async def get_user(
        user_id: int,
        session: AsyncSession,
) -> Sequence[User]:
    stmt = select(User).where(User.id==user_id)
    result = await session.scalars(stmt)
    return result.all()

async def get_all_users(
        session: AsyncSession
    ) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_user(
        user_create: CreateUser,
        session: AsyncSession
    ):
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    return user
