from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.comment_repository import CommentRepository
from src.repositories.post_repository import PostRepository
from src.repositories.user_repository import UserRepository
from src.core.exceptions.exceptions import (
    NotFoundException,
    ValidationException
)


class CommentService:

    def __init__(self, db: AsyncSession):
        self.repo = CommentRepository(db)
        self.post_repo = PostRepository(db)
        self.user_repo = UserRepository(db)

    async def get_comments(self):
        return await self.repo.get_all()

    async def get_comment(self, comment_id: int):
        comment = await self.repo.get_by_id(comment_id)

        if not comment:
            raise NotFoundException(
                "Comment not found",
                {"comment_id": comment_id}
            )

        return comment

    async def create_comment(self, data: dict):
        post = await self.post_repo.get_by_id(data["post_id"])
        if not post:
            raise NotFoundException(
                "Post not found",
                {"post_id": data["post_id"]}
            )

        user = await self.user_repo.get_by_id(data["author_id"])
        if not user:
            raise NotFoundException(
                "Author not found",
                {"author_id": data["author_id"]}
            )

        if not data["text"] or len(data["text"].strip()) == 0:
            raise ValidationException(
                "Comment text cannot be empty"
            )

        return await self.repo.create(data)

    async def update_comment(self, comment_id: int, data: dict):
        comment = await self.repo.update(comment_id, data)

        if not comment:
            raise NotFoundException(
                "Comment not found",
                {"comment_id": comment_id}
            )

        return comment

    async def delete_comment(self, comment_id: int):
        success = await self.repo.delete(comment_id)

        if not success:
            raise NotFoundException(
                "Comment not found",
                {"comment_id": comment_id}
            )

        return True
