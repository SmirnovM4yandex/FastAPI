from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.models.category_model import Category
from src.core.exceptions.exceptions import DatabaseException

logger = logging.getLogger(__name__)

class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        try:
            result = await self.db.execute(select(Category))
            return result.scalars().all()
        except SQLAlchemyError as ex:
            logger.error("Failed to fetch categories: %s", ex)
            raise DatabaseException(str(ex))

    async def get_by_id(self, category_id: int):
        try:
            result = await self.db.execute(select(Category).where(Category.id == category_id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as ex:
            logger.error("Failed to fetch category id=%s: %s", category_id, ex)
            raise DatabaseException(str(ex))

    async def create(self, data: dict):
        try:
            category = Category(**data)
            self.db.add(category)
            await self.db.commit()
            await self.db.refresh(category)
            logger.info("Created category id=%s", category.id)
            return category
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to create category: %s", ex)
            raise DatabaseException(str(ex))

    async def update(self, category_id: int, data: dict):
        try:
            category = await self.get_by_id(category_id)
            if not category:
                return None
            for key, value in data.items():
                if hasattr(category, key):
                    setattr(category, key, value)
            await self.db.commit()
            await self.db.refresh(category)
            logger.info("Updated category id=%s", category_id)
            return category
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to update category id=%s: %s", category_id, ex)
            raise DatabaseException(str(ex))

    async def delete(self, category_id: int):
        try:
            category = await self.get_by_id(category_id)
            if not category:
                return False
            await self.db.delete(category)
            await self.db.commit()
            logger.info("Deleted category id=%s", category_id)
            return True
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to delete category id=%s: %s", category_id, ex)
            raise DatabaseException(str(ex))