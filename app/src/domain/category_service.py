from sqlalchemy.ext.asyncio import AsyncSession

from src.models.category_model import Category
from src.repositories.category_repository import CategoryRepository
from src.core.exceptions.exceptions import (
    NotFoundException,
    ConflictException,
    ValidationException
)


class CategoryService:

    def __init__(self, db: AsyncSession):
        self.repo = CategoryRepository(db)

    async def get_categories(self):
        return await self.repo.get_all()

    async def get_category(self, category_id: int):
        category = await self.repo.get_by_id(category_id)

        if not category:
            raise NotFoundException("Category not found")

        return category

    async def create_category(self, data: dict):
        slug = data.get("slug")

        if not slug or not slug.strip():
            raise ValidationException("Slug cannot be empty")

        existing = await self.repo.get_by_slug(slug)

        if existing:
            raise ConflictException("Category slug must be unique")

        return await self.repo.create(data)

    async def update_category(self, category_id: int, data: dict, current_user):
        if not current_user.is_superuser:
            raise ConflictException("Only superuser can update categories")

        if "slug" in data:
            existing = await self.repo.get_by_slug(data["slug"])

            if existing and existing.id != category_id:
                raise ConflictException("Category slug must be unique")
    
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