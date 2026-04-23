from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.comment_repository import CommentRepository
from src.repositories.post_repository import PostRepository

from src.core.exceptions.exceptions import (
    NotFoundException,
    ValidationException,
    ConflictException
)


class CommentService:

    def __init__(self, db: AsyncSession):
        self.repo = CommentRepository(db)
        self.post_repo = PostRepository(db)

    async def get_comments(self):
        return await self.repo.get_all()

    async def get_comment(self, comment_id: int):
        comment = await self.repo.get_by_id(comment_id)

        if not comment:
            raise NotFoundException("Comment not found", {"comment_id": comment_id})

        return comment

    async def create_comment(self, data: dict, current_user):
        post = await self.post_repo.get_by_id(data["post_id"])

        if not post:
            raise NotFoundException("Post not found")

        if not data["text"] or len(data["text"].strip()) == 0:
            raise ValidationException("Comment text cannot be empty")

        data["author_id"] = current_user.id

        return await self.repo.create(data)

    async def update_comment(self, comment_id: int, data: dict, current_user):
        comment = await self.repo.get_by_id(comment_id)

        if not comment:
            raise NotFoundException("Comment not found")

        if comment.author_id != current_user.id and not current_user.is_superuser:
            raise ConflictException("No permission to update this comment")

        return await self.repo.update(comment_id, data)

    async def delete_comment(self, comment_id: int, current_user):
        comment = await self.repo.get_by_id(comment_id)

        if not comment:
            raise NotFoundException("Comment not found")

        if comment.author_id != current_user.id and not current_user.is_superuser:
            raise ConflictException("No permission to delete this comment")

        return await self.repo.delete(comment_id)