from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.blogicum_schemas import UserSchema, UserCreateSchema
from src.repositories.user_repository import UserRepository
from src.dependencies.database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return await repo.get_all()


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    user = await repo.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/", response_model=UserSchema, status_code=201)
async def create_user(data: UserCreateSchema, db:
                      AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    payload = data.model_dump()
    payload["password"] = data.password.get_secret_value()

    return await repo.create(payload)


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, data: UserCreateSchema, db:
                      AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    payload = data.model_dump()
    payload["password"] = data.password.get_secret_value()

    user = await repo.update(user_id, payload)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    success = await repo.delete(user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")
