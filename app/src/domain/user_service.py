from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_repository import UserRepository
from src.repositories.post_repository import PostRepository
from src.repositories.comment_repository import CommentRepository
from src.core.exceptions.exceptions import (
    NotFoundException,
    ConflictException,
    ValidationException
)
from src.resources.auth import get_password_hash


class UserService:

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.post_repo = PostRepository(db)
        self.comment_repo = CommentRepository(db)

    async def get_users(self):
        return await self.repo.get_all()

    async def get_user(self, user_id: int):
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise NotFoundException("User not found", {"user_id": user_id})

        return user

    async def get_user_by_login(self, login: str):
        user = await self.repo.get_by_username(login)

        if not user:
            raise NotFoundException("User not found", {"login": login})

        return user

    async def create_user(self, data: dict):
        if await self.repo.get_by_username(data["username"]):
            raise ConflictException("Username already exists")

        if await self.repo.get_by_email(data["email"]):
            raise ConflictException("Email already exists")

        if len(data["username"].strip()) < 3:
            raise ValidationException("Username too short")

        if len(data["password"]) < 6:
            raise ValidationException("Password too short")

        data["password"] = get_password_hash(data["password"])
        data["is_superuser"] = data.get("is_superuser", False)
        return await self.repo.create(data)

    async def update_user(self, user_id: int, data: dict, current_user):
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise NotFoundException("User not found")

        if user.id != current_user.id and not current_user.is_superuser:
            raise ConflictException("No permission to update this user")

        if "username" in data:
            existing = await self.repo.get_by_username(data["username"])
            if existing and existing.id != user_id:
                raise ConflictException("Username already exists")

        if "email" in data:
            existing = await self.repo.get_by_email(data["email"])
            if existing and existing.id != user_id:
                raise ConflictException("Email already exists")

        if "password" in data:
            if len(data["password"]) < 6:
                raise ValidationException("Password too short")
            data["password"] = get_password_hash(data["password"])

        return await self.repo.update(user_id, data)

    async def delete_user(self, user_id: int, current_user):
        user = await self.repo.get_by_id(user_id)

        if not user:
            raise NotFoundException("User not found")

        if user.id != current_user.id and not current_user.is_superuser:
            raise ConflictException("No permission to delete this user")

        comments = await self.comment_repo.get_all()
        for comment in comments:
            if comment.author_id == user_id:
                await self.comment_repo.delete(comment.id)

        posts = await self.post_repo.get_all()
        for post in posts:
            if post.author_id == user_id:
                post_comments = await self.comment_repo.get_all()
                for comment in post_comments:
                    if comment.post_id == post.id:
                        await self.comment_repo.delete(comment.id)
                await self.post_repo.delete(post.id)

        return await self.repo.delete(user_id)