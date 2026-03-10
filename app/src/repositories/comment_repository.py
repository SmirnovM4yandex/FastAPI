from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comment_model import Comment


class CommentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_post(self, post_id: int):
        result = await self.session.execute(
            select(Comment).where(Comment.post_id == post_id)
        )
        return result.scalars().all()

    async def create(self, data: dict):
        comment = Comment(**data)
        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)
        return comment
