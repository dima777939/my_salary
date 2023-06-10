from __future__ import annotations
from pydantic import BaseModel
from pydantic import EmailStr
from datetime import date


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool


class UserInfo(UserBase):
    rate_an_hour: int
    date_increased: date


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
