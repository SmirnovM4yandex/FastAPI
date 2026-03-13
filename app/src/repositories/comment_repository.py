from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comment_model import Comment


class CommentRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Comment))
        return result.scalars().all()

    async def get_by_id(self, comment_id: int):
        result = await self.db.execute(
            select(Comment).where(Comment.id == comment_id)
        )
        return result.scalar_one_or_none()

    async def get_by_post(self, post_id: int):
        result = await self.db.execute(
            select(Comment).where(Comment.post_id == post_id)
        )
        return result.scalars().all()

    async def create(self, data: dict):
        comment = Comment(**data)
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def update(self, comment_id: int, data: dict):
        comment = await self.get_by_id(comment_id)

        if not comment:
            return None

        for key, value in data.items():
            setattr(comment, key, value)

        await self.db.commit()
        await self.db.refresh(comment)

        return comment

    async def delete(self, comment_id: int):
        comment = await self.get_by_id(comment_id)

        if not comment:
            return False

        await self.db.delete(comment)
        await self.db.commit()

        return True
