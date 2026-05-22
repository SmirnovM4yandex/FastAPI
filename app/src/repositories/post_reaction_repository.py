import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.post_reaction_model import PostReaction
from src.core.exceptions.exceptions import DatabaseException

logger = logging.getLogger(__name__)


class PostReactionRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_reaction(self, post_id: int, user_id: int):
        try:
            result = await self.db.execute(
                select(PostReaction).where(
                    PostReaction.post_id == post_id,
                    PostReaction.user_id == user_id
                )
            )

            return result.scalar_one_or_none()

        except SQLAlchemyError as ex:
            logger.error("Failed to fetch reaction: %s", ex)
            raise DatabaseException(str(ex))

    async def create(self, post_id: int, user_id: int, value: int):
        try:
            reaction = PostReaction(
                post_id=post_id,
                user_id=user_id,
                value=value
            )

            self.db.add(reaction)

            await self.db.flush()
            await self.db.refresh(reaction)

            return reaction

        except SQLAlchemyError as ex:
            logger.error("Failed to create reaction: %s", ex)
            raise DatabaseException(str(ex))

    async def update(self, reaction):
        self.db.add(reaction)
        await self.db.flush()

    async def delete(self, reaction: PostReaction):
        try:
            await self.db.delete(reaction)

        except SQLAlchemyError as ex:
            logger.error("Failed to delete reaction: %s", ex)
            raise DatabaseException(str(ex))
