from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_repository import UserRepository
from src.core.exceptions.exceptions import (
    NotFoundException,
    ConflictException,
    ValidationException
)


class UserService:

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def get_users(self):
        return await self.repo.get_all()

    async def get_user(self, user_id: int):
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise NotFoundException(
                "User not found",
                {"user_id": user_id}
            )

        return user

    async def create_user(self, data: dict):
        if await self.repo.get_by_username(data["username"]):
            raise ConflictException(
                "Username already exists",
                {"username": data["username"]}
            )

        if await self.repo.get_by_email(data["email"]):
            raise ConflictException(
                "Email already exists",
                {"email": data["email"]}
            )

        if len(data["username"].strip()) < 3:
            raise ValidationException("Username too short")

        if len(data["password"]) < 6:
            raise ValidationException("Password too short")

        return await self.repo.create(data)

    async def update_user(self, user_id: int, data: dict):
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise NotFoundException(
                "User not found",
                {"user_id": user_id}
            )

        if "username" in data:
            existing = await self.repo.get_by_username(data["username"])
            if existing and existing.id != user_id:
                raise ConflictException(
                    "Username already exists",
                    {"username": data["username"]}
                )

        if "email" in data:
            existing = await self.repo.get_by_email(data["email"])
            if existing and existing.id != user_id:
                raise ConflictException(
                    "Email already exists",
                    {"email": data["email"]}
                )

        if "username" in data and len(data["username"].strip()) < 3:
            raise ValidationException("Username too short")

        if "password" in data and len(data["password"]) < 6:
            raise ValidationException("Password too short")

        return await self.repo.update(user_id, data)

    async def delete_user(self, user_id: int):
        success = await self.repo.delete(user_id)

        if not success:
            raise NotFoundException(
                "User not found",
                {"user_id": user_id}
            )

        return True
