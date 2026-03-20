from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from src.models.category_model import Category
from src.repositories.category_repository import CategoryRepository


class CategoryService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CategoryRepository(db)

    async def get_categories(self):
        return await self.repo.get_all()

    async def get_category(self, category_id: int):
        return await self.repo.get_by_id(category_id)

    async def create_category(self, data: dict):

        existing = await self.db.execute(
            select(Category).where(Category.slug == data["slug"])
        )

        if existing.scalar_one_or_none():
            raise HTTPException(409, "Category slug must be unique")
        
        if len(data["slug"]) < 1:
            raise HTTPException(411, "Category name empty")

        return await self.repo.create(data)

    async def update_category(self, category_id: int, data: dict):
        return await self.repo.update(category_id, data)

    async def delete_category(self, category_id: int):
        return await self.repo.delete(category_id)
