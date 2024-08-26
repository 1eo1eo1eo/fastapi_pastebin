from fastapi import APIRouter, Depends
from typing import Annotated, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from crud import users as users_crud
from users.schemas import CreateUser, ReadUser

from core.models import db_helper


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/{user_id}", response_model=list[ReadUser])
async def get_user(
    user_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ]
):
    user = await users_crud.get_user(
        user_id=user_id,
        session=session,
    )
    return user

@router.get("", response_model=list[ReadUser])
async def get_users(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ]
):
    users = await users_crud.get_all_users(session=session)
    return users

@router.post("", response_model=ReadUser)
async def create_user(
    user_create: CreateUser,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ]
):
    user = await users_crud.create_user(
        session=session,
        user_create=user_create,
    )
    return user