from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.post_model import Post


class PostRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Post))
        return result.scalars().all()

    async def get_by_id(self, post_id: int):
        result = await self.db.execute(
            select(Post).where(Post.id == post_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: dict):
        post = Post(**data)

        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)

        return post

    async def update(self, post_id: int, data: dict):
        post = await self.get_by_id(post_id)

        if not post:
            return None

        for key, value in data.items():
            if hasattr(post, key):
                setattr(post, key, value)

        await self.db.commit()
        await self.db.refresh(post)

        return post

    async def delete(self, post_id: int):
        post = await self.get_by_id(post_id)

        if not post:
            return False

        await self.db.delete(post)
        await self.db.commit()

        return True
