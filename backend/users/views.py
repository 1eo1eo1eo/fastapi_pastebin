from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from users import crud as users_crud
from users.schemas import UserCreate, UserUpdate, UserUpdatePartial
from users.schemas import User as response_user
from users.dependencies import product_by_id

from core.models import db_helper
from .models import User


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/{user_id}", response_model=response_user)
async def get_user(user: User = Depends(product_by_id)):
    return user


@router.get("", response_model=list[response_user])
async def get_users(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ]
):
    users = await users_crud.get_all_users(session=session)
    return users


@router.post("", response_model=response_user, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    user = await users_crud.create_user(
        session=session,
        user_create=user_create,
    )
    return user


@router.put("/{user_id}", response_model=response_user)
async def update_user(
    user: Annotated[User, Depends(product_by_id)],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user_update: UserUpdate,
):
    return await users_crud.update_user(
        session=session,
        user=user,
        user_update=user_update,
    )


@router.patch("/{user_id}", response_model=response_user)
async def update_user_partial(
    user: Annotated[User, Depends(product_by_id)],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user_update_partial: UserUpdatePartial,
):
    return await users_crud.update_user_partial(
        session=session,
        user=user,
        user_update_partial=user_update_partial,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: Annotated[
        User,
        Depends(product_by_id),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> None:
    return await users_crud.delete_user(
        session=session,
        user=user,
    )
