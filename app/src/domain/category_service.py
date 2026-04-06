from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.category_model import Category
from src.repositories.category_repository import CategoryRepository
from src.core.exceptions.exceptions import (
    NotFoundException,
    ConflictException,
    ValidationException
)


class CategoryService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CategoryRepository(db)

    async def get_categories(self):
        return await self.repo.get_all()

    async def get_category(self, category_id: int):
        category = await self.repo.get_by_id(category_id)

        if not category:
            raise NotFoundException(
                "Category not found",
                {"category_id": category_id}
            )

        return category

    async def create_category(self, data: dict):
        if not data["slug"] or len(data["slug"].strip()) == 0:
            raise ValidationException(
                "Slug cannot be empty",
                {"slug": data.get("slug")}
            )

        existing = await self.db.execute(
            select(Category).where(Category.slug == data["slug"])
        )

        if existing.scalar_one_or_none():
            raise ConflictException(
                "Category slug must be unique",
                {"slug": data["slug"]}
            )

        return await self.repo.create(data)

    async def update_category(self, category_id: int, data: dict):
        category = await self.repo.update(category_id, data)

        if not category:
            raise NotFoundException(
                "Category not found",
                {"category_id": category_id}
            )

        return category

    async def delete_category(self, category_id: int):
        success = await self.repo.delete(category_id)

        if not success:
            raise NotFoundException(
                "Category not found",
                {"category_id": category_id}
            )

        return True
