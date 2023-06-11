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
    is_staff: bool = False
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str
    rate_an_hour: int
    date_increased: date


class UserUpdateRequest(BaseModel):
    first_name: str | None
    last_name: str | None
    email: EmailStr | None
    rate_an_hour: int | None
    date_increased: date | None


class UserInfo(UserBase):
    rate_an_hour: int
    date_increased: date


class UserDB(UserBase):
    id: int
    hashed_password: str
    rate_an_hour: int
    date_increased: date

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
