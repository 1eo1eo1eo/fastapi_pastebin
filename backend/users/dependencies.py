from typing import Annotated

from fastapi import Depends, Path, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .models import User
from users import crud as users_crud


async def product_by_id(
    user_id: Annotated[int, Path],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> User:
    user = await users_crud.get_user(
        user_id=user_id,
        session=session,
    )
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )
