from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging

from src.models.user_model import User
from src.core.exceptions.exceptions import DatabaseException

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        try:
            result = await self.db.execute(select(User))
            return result.scalars().all()
        except SQLAlchemyError as ex:
            logger.error("Failed to fetch users: %s", ex)
            raise DatabaseException(str(ex))

    async def get_by_id(self, user_id: int):
        try:
            result = await self.db.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as ex:
            logger.error("Failed to fetch user id=%s: %s", user_id, ex)
            raise DatabaseException(str(ex))

    async def get_by_username(self, username: str):
        try:
            result = await self.db.execute(select(User).where(User.username == username))
            return result.scalar_one_or_none()
        except SQLAlchemyError as ex:
            logger.error("Failed to fetch user by username=%s: %s", username, ex)
            raise DatabaseException(str(ex))

    async def get_by_email(self, email: str):
        try:
            result = await self.db.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()
        except SQLAlchemyError as ex:
            logger.error("Failed to fetch user by email=%s: %s", email, ex)
            raise DatabaseException(str(ex))

    async def create(self, data: dict):
        try:
            now = datetime.now()
            user = User(
                username=data["username"],
                email=data["email"],
                password=data["password"],
                first_name=data.get("first_name") or "",
                last_name=data.get("last_name") or "",
                date_joined=now,
                last_login=None,
                is_superuser=data.get("is_superuser", False),
                is_staff=False,
                is_active=True
            )
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            logger.info("Created user id=%s", user.id)
            return user
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to create user: %s", ex)
            raise DatabaseException(str(ex))

    async def update(self, user_id: int, data: dict):
        try:
            user = await self.get_by_id(user_id)
            if not user:
                return None
            for key, value in data.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            await self.db.commit()
            await self.db.refresh(user)
            logger.info("Updated user id=%s", user_id)
            return user
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to update user id=%s: %s", user_id, ex)
            raise DatabaseException(str(ex))

    async def delete(self, user_id: int):
        try:
            user = await self.get_by_id(user_id)
            if not user:
                return False
            await self.db.delete(user)
            await self.db.commit()
            logger.info("Deleted user id=%s", user_id)
            return True
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to delete user id=%s: %s", user_id, ex)
            raise DatabaseException(str(ex))