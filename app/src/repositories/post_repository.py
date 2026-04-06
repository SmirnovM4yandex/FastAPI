from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.models.post_model import Post
from src.core.exceptions.exceptions import DatabaseException

logger = logging.getLogger(__name__)

class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        try:
            result = await self.db.execute(select(Post))
            return result.scalars().all()
        except SQLAlchemyError as ex:
            logger.error("Failed to fetch posts: %s", ex)
            raise DatabaseException(str(ex))

    async def get_by_id(self, post_id: int):
        try:
            result = await self.db.execute(select(Post).where(Post.id == post_id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as ex:
            logger.error("Failed to fetch post id=%s: %s", post_id, ex)
            raise DatabaseException(str(ex))

    async def create(self, data: dict):
        try:
            post = Post(**data)
            self.db.add(post)
            await self.db.commit()
            await self.db.refresh(post)
            logger.info("Created post id=%s", post.id)
            return post
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to create post: %s", ex)
            raise DatabaseException(str(ex))

    async def update(self, post_id: int, data: dict):
        try:
            post = await self.get_by_id(post_id)
            if not post:
                return None
            for key, value in data.items():
                if hasattr(post, key):
                    setattr(post, key, value)
            await self.db.commit()
            await self.db.refresh(post)
            logger.info("Updated post id=%s", post_id)
            return post
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to update post id=%s: %s", post_id, ex)
            raise DatabaseException(str(ex))

    async def delete(self, post_id: int):
        try:
            post = await self.get_by_id(post_id)
            if not post:
                return False
            await self.db.delete(post)
            await self.db.commit()
            logger.info("Deleted post id=%s", post_id)
            return True
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to delete post id=%s: %s", post_id, ex)
            raise DatabaseException(str(ex))