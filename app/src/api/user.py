from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_schemas import UserSchema, UserCreateSchema
from src.dependencies.database import get_db
from src.domain.user_service import UserService
from src.domain.auth_service import AuthService
from src.core.exceptions.exceptions import (
    NotFoundException,
    ConflictException,
)

router = APIRouter()


@router.get(
    "/{login}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def get_user_by_login(
    login: str,
    current_user: UserSchema = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserSchema:
    try:
        return await UserService(db).get_user_by_login(login)
    except NotFoundException as exc:
        exc.log()
        raise HTTPException(status_code=404, detail=exc.message)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchema,
)
async def create_user(
    user: UserCreateSchema,
    db: AsyncSession = Depends(get_db),
) -> UserSchema:
    try:
        payload = user.model_dump()
        payload["password"] = user.password.get_secret_value()

        return await UserService(db).create_user(payload)
    except ConflictException as exc:
        exc.log()
        raise HTTPException(status_code=409, detail=exc.message)
