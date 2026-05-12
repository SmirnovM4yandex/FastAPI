from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exception_handler import handle_exception
from src.core.exceptions.exceptions import (
    ConflictException,
    NotFoundException,
)
from src.dependencies.database import get_db
from src.domain.auth_service import AuthService
from src.domain.user_service import UserService
from src.schemas.user_schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponseSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        return await UserService(db).get_users()
    except Exception as ex:
        handle_exception(ex)


@router.get("/id/{user_id}", response_model=UserResponseSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await UserService(db).get_user(user_id)
    except Exception as ex:
        handle_exception(ex)


@router.get("/login/{login}", response_model=UserResponseSchema)
async def get_user_by_login(login: str, db: AsyncSession = Depends(get_db)):
    try:
        return await UserService(db).get_user_by_login(login)
    except NotFoundException as exc:
        exc.log()
        raise HTTPException(status_code=404, detail=exc.message)


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
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

    except Exception as ex:
        handle_exception(ex)


@router.put("/{user_id}", response_model=UserResponseSchema)
async def update_user(
    user_id: int,
    data: UserCreateSchema,
    current_user=Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        payload = data.model_dump()

        payload["password"] = data.password.get_secret_value()

        return await UserService(db).update_user(
            user_id=user_id,
            data=payload,
            current_user=current_user,
        )

    except Exception as ex:
        handle_exception(ex)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    data: UserUpdateSchema,
    current_user=Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await UserService(db).delete_user(user_id, current_user)

    except Exception as ex:
        handle_exception(ex)