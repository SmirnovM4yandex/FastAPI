from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.post_model import Post


class PostRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        query = select(Post)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, post_id: int):
        query = select(Post).where(Post.id == post_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: dict):
        post = Post(**data)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def update(self, post_id: int, data: dict):
        post = await self.get_by_id(post_id)
        if not post:
            return None

        for field, value in data.items():
            setattr(post, field, value)

        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def delete(self, post_id: int):
        post = await self.get_by_id(post_id)
        if not post:
            return False

        await self.session.delete(post)
        await self.session.commit()
        return True
