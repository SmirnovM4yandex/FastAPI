from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.comment_repository import CommentRepository
from src.repositories.post_repository import PostRepository
from src.repositories.user_repository import UserRepository


class CommentService:

    def __init__(self, db: AsyncSession):
        self.repo = CommentRepository(db)
        self.post_repo = PostRepository(db)
        self.user_repo = UserRepository(db)

    async def get_comments(self):
        return await self.repo.get_all()

    async def get_comment(self, comment_id: int):
        return await self.repo.get_by_id(comment_id)

    async def create_comment(self, data: dict):

        if not await self.post_repo.get_by_id(data["post_id"]):
            raise ValueError("Post not found")

        if not await self.user_repo.get_by_id(data["author_id"]):
            raise ValueError("Author not found")

        if len(data["text"]) < 1:
            raise ValueError("Comment text empty")

        return await self.repo.create(data)

    async def update_comment(self, comment_id: int, data: dict):
        return await self.repo.update(comment_id, data)

    async def delete_comment(self, comment_id: int):
        return await self.repo.delete(comment_id)
