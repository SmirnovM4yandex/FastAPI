import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.post_model import Post
from src.core.exceptions.exceptions import DatabaseException

logger = logging.getLogger(__name__)


class PostRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        try:
            result = await self.db.execute(
                select(Post).order_by(Post.id)
            )
            return result.scalars().all()

        except SQLAlchemyError as ex:
            logger.error("Failed to fetch posts: %s", ex)
            raise DatabaseException(str(ex))

    async def get_by_id(self, post_id: int):
        try:
            result = await self.db.execute(
                select(Post).where(Post.id == post_id)
            )
            return result.scalar_one_or_none()

        except SQLAlchemyError as ex:
            logger.error("Failed to fetch post id=%s: %s", post_id, ex)
            raise DatabaseException(str(ex))

    async def get_by_author(self, author_id: int):
        result = await self.db.execute(
            select(Post).where(Post.author_id == author_id)
        )
        return result.scalars().all()

    async def create(self, data: dict):
        try:
            post = Post(**data)

            self.db.add(post)

            await self.db.flush()
            await self.db.refresh(post)

            logger.info("Created post id=%s", post.id)

            return post

        except SQLAlchemyError as ex:
            logger.error("Failed to create post: %s", ex)
            raise DatabaseException(str(ex))

    async def update(self, post_id: int, data: dict):
        try:
            post = await self.get_by_id(post_id)

            if not post:
                return None

            for key, value in data.items():
                if hasattr(post, key) and value is not None:
                    setattr(post, key, value)

            await self.db.flush()
            await self.db.refresh(post)

            logger.info("Updated post id=%s", post_id)

            return post

        except SQLAlchemyError as ex:
            logger.error("Failed to update post id=%s: %s", post_id, ex)
            raise DatabaseException(str(ex))

    async def delete(self, post_id: int):
        try:
            post = await self.get_by_id(post_id)

            if not post:
                return False

            await self.db.delete(post)

            logger.info("Deleted post id=%s", post_id)

            return True

        except SQLAlchemyError as ex:
            logger.error("Failed to delete post id=%s: %s", post_id, ex)
            raise DatabaseException(str(ex))