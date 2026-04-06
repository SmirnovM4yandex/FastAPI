from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging

from src.models.comment_model import Comment
from src.core.exceptions.exceptions import DatabaseException

logger = logging.getLogger(__name__)

class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        try:
            result = await self.db.execute(select(Comment))
            return result.scalars().all()
        except SQLAlchemyError as ex:
            logger.error("Failed to fetch comments: %s", ex)
            raise DatabaseException(str(ex))

    async def get_by_id(self, comment_id: int):
        try:
            result = await self.db.execute(select(Comment).where(Comment.id == comment_id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as ex:
            logger.error("Failed to fetch comment id=%s: %s", comment_id, ex)
            raise DatabaseException(str(ex))

    async def get_by_post(self, post_id: int):
        try:
            result = await self.db.execute(select(Comment).where(Comment.post_id == post_id))
            return result.scalars().all()
        except SQLAlchemyError as ex:
            logger.error("Failed to fetch comments for post id=%s: %s", post_id, ex)
            raise DatabaseException(str(ex))

    async def create(self, data: dict):
        try:
            comment = Comment(**data)
            self.db.add(comment)
            await self.db.commit()
            await self.db.refresh(comment)
            logger.info("Created comment id=%s", comment.id)
            return comment
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to create comment: %s", ex)
            raise DatabaseException(str(ex))

    async def update(self, comment_id: int, data: dict):
        try:
            comment = await self.get_by_id(comment_id)
            if not comment:
                return None
            for key, value in data.items():
                if hasattr(comment, key):
                    setattr(comment, key, value)
            await self.db.commit()
            await self.db.refresh(comment)
            logger.info("Updated comment id=%s", comment_id)
            return comment
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to update comment id=%s: %s", comment_id, ex)
            raise DatabaseException(str(ex))

    async def delete(self, comment_id: int):
        try:
            comment = await self.get_by_id(comment_id)
            if not comment:
                return False
            await self.db.delete(comment)
            await self.db.commit()
            logger.info("Deleted comment id=%s", comment_id)
            return True
        except SQLAlchemyError as ex:
            await self.db.rollback()
            logger.error("Failed to delete comment id=%s: %s", comment_id, ex)
            raise DatabaseException(str(ex))