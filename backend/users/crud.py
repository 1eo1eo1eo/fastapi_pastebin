from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from users.schemas import UserCreate, UserUpdate, UserUpdatePartial
from users.models import User


async def get_user(
        session: AsyncSession,
        user_id: int,
) -> User | None:
    return await session.get(User, user_id)

async def get_all_users(
        session: AsyncSession,
    ) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_user(
        session: AsyncSession,
        user_create: UserCreate,
    ) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    return user


async def update_user(
        session: AsyncSession,
        user: User,
        user_update: UserUpdate,
) -> User:
    for name, value in user_update.model_dump().items():
        setattr(user, name, value)
    await session.commit()
    return user


async def update_user_partial(
        session: AsyncSession,
        user: User,
        user_update_partial: UserUpdatePartial,
) -> User:
    for name, value in user_update_partial.model_dump(exclude_unset=True).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(
        session: AsyncSession,
        user: User,
) -> None:
    await session.delete(user)
    await session.commit()