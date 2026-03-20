from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from src.models.user_model import User
from src.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UserRepository(db)

    async def get_users(self):
        return await self.repo.get_all()

    async def get_user(self, user_id: int):
        return await self.repo.get_by_id(user_id)

    async def create_user(self, data: dict):

        existing = await self.db.execute(
            select(User).where(User.username == data["username"])
        )

        if existing.scalar_one_or_none():
            raise HTTPException(401, "Username already exists")

        existing_email = await self.db.execute(
            select(User).where(User.email == data["email"])
        )

        if existing_email.scalar_one_or_none():
            raise HTTPException(401, "Email already exists")

        return await self.repo.create(data)

    async def update_user(self, user_id: int, data: dict):
        return await self.repo.update(user_id, data)

    async def delete_user(self, user_id: int):
        return await self.repo.delete(user_id)
