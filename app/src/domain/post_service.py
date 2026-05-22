from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.post_repository import PostRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.location_repository import LocationRepository
from src.repositories.post_reaction_repository import PostReactionRepository

from src.core.exceptions.exceptions import (
    NotFoundException,
    ValidationException,
    ConflictException
)


class PostService:

    def __init__(self, db: AsyncSession):
        self.repo = PostRepository(db)
        self.category_repo = CategoryRepository(db)
        self.location_repo = LocationRepository(db)
        self.reaction_repo = PostReactionRepository(db)

    async def get_posts(self):
        return await self.repo.get_all()

    async def get_post(self, post_id: int):
        post = await self.repo.get_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found", {"post_id": post_id})

        return post

    async def create_post(self, data: dict, current_user):
        data["author_id"] = current_user.id

        if not data.get("title") or len(data["title"].strip()) < 3:
            raise ValidationException("Title must be at least 3 characters")

        if data.get("category_id") and not await self.category_repo.get_by_id(data["category_id"]):
            raise NotFoundException("Category not found")

        if data.get("location_id") and not await self.location_repo.get_by_id(data["location_id"]):
            raise NotFoundException("Location not found")

        return await self.repo.create(data)

    async def update_post(self, post_id: int, data: dict, current_user):
        post = await self.repo.get_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found", {"post_id": post_id})

        if post.author_id != current_user.id and not current_user.is_superuser:
            raise ConflictException("No permission to update this post")

        if "category_id" in data and data["category_id"]:
            if not await self.category_repo.get_by_id(data["category_id"]):
                raise NotFoundException("Category not found")

        if "location_id" in data and data["location_id"]:
            if not await self.location_repo.get_by_id(data["location_id"]):
                raise NotFoundException("Location not found")

        return await self.repo.update(post_id, data)

    async def delete_post(self, post_id: int, current_user):
        post = await self.repo.get_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found", {"post_id": post_id})

        if post.author_id != current_user.id and not current_user.is_superuser:
            raise ConflictException("No permission to delete this post")

        return await self.repo.delete(post_id)

    async def react_to_post(
        self,
        post_id: int,
        value: int,
        current_user
    ):
        post = await self.repo.get_by_id(post_id)

        if not post:
            raise NotFoundException("Post not found")

        if value not in [1, -1]:
            raise ValidationException("Invalid reaction")

        existing = await self.reaction_repo.get_user_reaction(
            post_id,
            current_user.id
        )

        if existing:
            if existing.value == value:
                await self.reaction_repo.delete(existing)

            else:
                existing.value = value
                await self.reaction_repo.update(existing)  # ВАЖНО

        else:
            await self.reaction_repo.create(
                post_id,
                current_user.id,
                value
            )

        await self.reaction_repo.db.commit()

        return await self.repo.get_by_id(post_id)
