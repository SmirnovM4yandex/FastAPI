from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.user_schemas import UserSchema, UserCreateSchema
from src.dependencies.database import get_db
from src.domain.user_service import UserService
from src.api.exception_handler import handle_exception
from src.domain.auth_service import AuthService
from src.core.exceptions.exceptions import (
    NotFoundException,
    ConflictException
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        return await UserService(db).get_users()
    except Exception as ex:
        handle_exception(ex)


@router.get("/id/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await UserService(db).get_user(user_id)
    except Exception as ex:
        handle_exception(ex)


@router.get("/login/{login}", response_model=UserSchema)
async def get_user_by_login(login: str, db: AsyncSession = Depends(get_db)):
    try:
        return await UserService(db).get_user_by_login(login)
    except NotFoundException as exc:
        exc.log()
        raise HTTPException(status_code=404, detail=exc.message)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create_user(
    user: UserCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = user.model_dump()
        payload["password"] = user.password.get_secret_value()

        return await UserService(db).create_user(payload)
    except ConflictException as exc:
        exc.log()
        raise HTTPException(status_code=409, detail=exc.message)


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int,
    data: UserCreateSchema,
    current_user: UserSchema = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = data.model_dump()
        if data.password:
            payload["password"] = data.password.get_secret_value()

        return await UserService(db).update_user(user_id, payload, current_user)
    except Exception as ex:
        handle_exception(ex)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: int,
    current_user: UserSchema = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await UserService(db).delete_user(user_id, current_user)
    except Exception as ex:
        handle_exception(ex)