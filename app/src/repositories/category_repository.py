from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.category_model import Category


class CategoryRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Category))
        return result.scalars().all()

    async def get_by_id(self, category_id: int):
        result = await self.db.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: dict):
        category = Category(**data)

        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)

        return category

    async def update(self, category_id: int, data: dict):
        category = await self.get_by_id(category_id)

        if not category:
            return None

        for key, value in data.items():
            if hasattr(category, key):
                setattr(category, key, value)

        await self.db.commit()
        await self.db.refresh(category)

        return category

    async def delete(self, category_id: int):
        category = await self.get_by_id(category_id)

        if not category:
            return False

        await self.db.delete(category)
        await self.db.commit()

        return True
