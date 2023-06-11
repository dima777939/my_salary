from __future__ import annotations

from sqlalchemy import select, and_


from .models import User
from .schemas import UserCreate, UserBase, UserInfo
from .utils import get_password_hash
from api.db import database as db


async def create_user(user: UserCreate) -> UserBase:
    hashed_password = get_password_hash(user.password)
    query = User.insert().values(
        username=user.username,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        rate_an_hour=user.rate_an_hour,
        date_increased=user.date_increased,
        is_staff=user.is_staff,
        is_superuser=user.is_superuser,
    )
    new_user = await db.execute(query)
    query_select = User.select().where(User.c.id == new_user)
    user_db = await db.fetch_one(query_select)
    return user_db


async def get_users(skip: int = 0, limit: int = 100) -> list[UserInfo]:
    query = select(User).offset(skip).limit(limit)
    return await db.fetch_all(query)


async def get_user(username: str) -> UserInfo:
    query = select(User).where(
        and_(User.c.username == username, User.c.is_active == True)
    )
    user_db = await db.fetch_one(query)
    return user_db


async def get_user_by_username_or_email(username: str, email: str) -> UserBase:
    user_db = await db.execute(select(User).where(User.c.username == username))
    if not user_db:
        user_db = await db.execute(select(User).where(User.c.email == email))
    return user_db


async def get_update_user(user_name: str, user_data: UserInfo):
    query = (
        User.update()
        .where(and_(User.c.username == user_name, User.c.is_active == True))
        .values(
            rate_an_hour=user_data.rate_an_hour, date_increased=user_data.date_increased
        )
    )
    return await db.fetch_one(query)


async def get_user_elevation(user_name: str, user_data: UserInfo) -> UserInfo:
    query = (
        User.update()
        .where(and_(User.c.username == user_name, User.c.is_active == True))
        .values(is_staff=user_data.is_staff)
    )
    return await db.fetch_one(query)


async def get_user_for_active(user_name) -> UserInfo:
    query = select(User).where(and_(User.c.username == user_name))
    return await db.fetch_one(query)


async def get_user_active(user_name: str, used_data: UserBase) -> UserInfo:
    query = (
        User.update()
        .where(and_(User.c.username == user_name))
        .values(is_active=used_data.is_active)
    )
    return await db.fetch_one(query)
