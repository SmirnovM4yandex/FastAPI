from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.user_schemas import UserSchema, UserCreateSchema
from src.dependencies.database import get_db
from src.domain.user_service import UserService
from src.api.exception_handler import handle_exception

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        return await UserService(db).get_users()
    except Exception as ex:
        handle_exception(ex)


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await UserService(db).get_user(user_id)
    except Exception as ex:
        handle_exception(ex)


@router.post("/", response_model=UserSchema, status_code=201)
async def create_user(data: UserCreateSchema,
                      db: AsyncSession = Depends(get_db)):
    try:
        payload = data.model_dump()
        payload["password"] = data.password.get_secret_value()

        return await UserService(db).create_user(payload)
    except Exception as ex:
        handle_exception(ex)


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int,
                      data: UserCreateSchema,
                      db: AsyncSession = Depends(get_db)):
    try:
        payload = data.model_dump()
        payload["password"] = data.password.get_secret_value()

        return await UserService(db).update_user(user_id, payload)
    except Exception as ex:
        handle_exception(ex)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int,
                      db: AsyncSession = Depends(get_db)):
    try:
        await UserService(db).delete_user(user_id)
    except Exception as ex:
        handle_exception(ex)