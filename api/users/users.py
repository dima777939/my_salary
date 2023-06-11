from datetime import timedelta
from typing import Annotated, Dict, Union, List

from .crud import *
from .dependencies import (
    get_current_active_user,
    get_current_staff_user,
    get_current_admin,
)
from .schemas import *

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from .utils import auth_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter()


@router.post("/register/", response_model=UserBase)
async def create_new_user(user: UserCreate):
    user_db = await get_user_by_username_or_email(user.username, user.email)
    if user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered.",
        )
    return await create_user(user)


@router.post("/auth/", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await auth_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserInfo)
async def get_user_salary(current_user: UserInfo = Depends(get_current_active_user)):
    user_info = await get_user(current_user.username)
    if user_info.username == current_user.username:
        return user_info


@router.get("/users/", response_model=Dict[str, Union[List[UserBase], UserBase]])
async def get_users_list(
    skip: int = 0,
    limit: int = 100,
    current_user: UserBase = Depends(get_current_staff_user),
):
    users = await get_users(skip=skip, limit=limit)
    return {"users": users, "current_user": current_user}


@router.get("/users/{user_name}", response_model=Dict[str, UserInfo])
async def get_user_for_update_salary(
    user_name: str, current_user: UserBase = Depends(get_current_staff_user)
):
    user_for_update = await get_user(user_name)
    if not user_for_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"user_for_update": user_for_update, "current_user": current_user}


@router.put("/users/{user_name}", response_model=Dict[str, UserInfo])
async def update_user_salary(
    user_name: str,
    user_data: UserInfo,
    current_user: UserBase = Depends(get_current_staff_user),
):
    user_for_update = await get_user(user_name)
    if not user_for_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await get_update_user(user_name, user_data)
    user_updated = await get_user(user_name)
    return {"user_updated": user_updated, "current_user": current_user}


@router.put("/users/upgrade/{user_name}", response_model=Dict[str, UserInfo])
async def upgrade_user_permission(
    user_name: str,
    user_data: UserInfo,
    current_user: UserBase = Depends(get_current_admin),
):
    user_for_update = await get_user(user_name)
    if not user_for_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await get_user_elevation(user_name, user_data)
    user_updated = await get_user(user_name)
    return {"user_updated": user_updated, "current_user": current_user}


@router.put("/users/activation/{user_name}", response_model=Dict[str, UserBase])
async def update_active_deactive(
    user_name: str,
    data_user: UserBase,
    current_user: UserBase = Depends(get_current_admin),
):
    user_for_update = await get_user_for_active(user_name)
    if not user_for_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await get_user_active(user_name, data_user)
    user_updated = await get_user_for_active(user_name)
    return {"user_updated": user_updated, "current_user": current_user}
