from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.post_repository import PostRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.location_repository import LocationRepository
from src.repositories.user_repository import UserRepository

from src.core.exceptions.exceptions import (
    NotFoundException,
    ValidationException
)


class PostService:

    def __init__(self, db: AsyncSession):
        self.repo = PostRepository(db)
        self.category_repo = CategoryRepository(db)
        self.location_repo = LocationRepository(db)
        self.user_repo = UserRepository(db)

    async def get_posts(self):
        return await self.repo.get_all()

    async def get_post(self, post_id: int):
        post = await self.repo.get_by_id(post_id)

        if not post:
            raise NotFoundException(
                "Post not found",
                {"post_id": post_id}
            )

        return post

    async def create_post(self, data: dict):
        if not await self.user_repo.get_by_id(data["author_id"]):
            raise NotFoundException(
                "Author not found",
                {"author_id": data["author_id"]}
            )

        if data.get("category_id") is not None:
            if not await self.category_repo.get_by_id(data["category_id"]):
                raise NotFoundException(
                    "Category not found",
                    {"category_id": data["category_id"]}
                )

        if data.get("location_id") is not None:
            if not await self.location_repo.get_by_id(data["location_id"]):
                raise NotFoundException(
                    "Location not found",
                    {"location_id": data["location_id"]}
                )

        if not data["title"] or len(data["title"].strip()) < 3:
            raise ValidationException(
                "Title must be at least 3 characters"
            )

        return await self.repo.create(data)

    async def update_post(self, post_id: int, data: dict):
        if not await self.user_repo.get_by_id(data["author_id"]):
            raise NotFoundException(
                "Author not found",
                {"author_id": data["author_id"]}
            )

        if data.get("category_id") is not None:
            if not await self.category_repo.get_by_id(data["category_id"]):
                raise NotFoundException(
                    "Category not found",
                    {"category_id": data["category_id"]}
                )

        if data.get("location_id") is not None:
            if not await self.location_repo.get_by_id(data["location_id"]):
                raise NotFoundException(
                    "Location not found",
                    {"location_id": data["location_id"]}
                )

        if not data["title"] or len(data["title"].strip()) < 3:
            raise ValidationException(
                "Title must be at least 3 characters"
            )

        post = await self.repo.update(post_id, data)

        if not post:
            raise NotFoundException(
                "Post not found",
                {"post_id": post_id}
            )

        return post

    async def delete_post(self, post_id: int):
        success = await self.repo.delete(post_id)

        if not success:
            raise NotFoundException(
                "Post not found",
                {"post_id": post_id}
            )

        return True
