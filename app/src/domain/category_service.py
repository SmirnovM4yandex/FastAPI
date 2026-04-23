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
            raise NotFoundException("Category not found")

        return category

    async def create_category(self, data: dict, current_user):
        if not data["slug"] or len(data["slug"].strip()) == 0:
            raise ValidationException("Slug cannot be empty")

        existing = await self.db.execute(
            select(Category).where(Category.slug == data["slug"])
        )

        if existing.scalar_one_or_none():
            raise ConflictException("Category slug must be unique")

        return await self.repo.create(data)

    async def update_category(self, category_id: int, data: dict, current_user):
        if not current_user.is_superuser:
            raise ConflictException("Only superuser can update categories")

        category = await self.repo.update(category_id, data)

        if not category:
            raise NotFoundException("Category not found")

        return category

    async def delete_category(self, category_id: int, current_user):
        if not current_user.is_superuser:
            raise ConflictException("Only superuser can delete categories")

        success = await self.repo.delete(category_id)

        if not success:
            raise NotFoundException("Category not found")

        return True