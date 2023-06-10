from __future__ import annotations

from sqlalchemy import select, and_


from .models import User
from .schemas import UserInfo
from api.db import database as db


async def get_user(username: str) -> UserInfo:
    query = select(User).where(
        and_(User.c.username == username, User.c.is_active == True)
    )
    user_db = await db.fetch_one(query)
    return user_db
