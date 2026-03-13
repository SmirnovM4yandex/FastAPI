from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from src.models.user_model import User


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, user_id: int):
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: dict):

        now = datetime.now()

        user = User(
            username=data["username"],
            email=data["email"],
            password=data["password"],

            first_name=data.get("first_name") or "",
            last_name=data.get("last_name") or "",

            date_joined=now,
            last_login=None,

            is_superuser=False,
            is_staff=False,
            is_active=True
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update(self, user_id: int, data: dict):

        user = await self.get_by_id(user_id)

        if not user:
            return None

        for key, value in data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def delete(self, user_id: int):

        user = await self.get_by_id(user_id)

        if not user:
            return False

        await self.db.delete(user)
        await self.db.commit()

        return True
