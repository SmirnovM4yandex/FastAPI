from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.post_repository import PostRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.location_repository import LocationRepository
from src.repositories.user_repository import UserRepository


class PostService:

    def __init__(self, db: AsyncSession):
        self.repo = PostRepository(db)
        self.category_repo = CategoryRepository(db)
        self.location_repo = LocationRepository(db)
        self.user_repo = UserRepository(db)

    async def get_posts(self):
        return await self.repo.get_all()

    async def get_post(self, post_id: int):
        return await self.repo.get_by_id(post_id)

    async def create_post(self, data: dict):

        if not await self.user_repo.get_by_id(data["author_id"]):
            raise ValueError("Author not found")

        if data.get("category_id"):
            if not await self.category_repo.get_by_id(data["category_id"]):
                raise ValueError("Category not found")

        if data.get("location_id"):
            if not await self.location_repo.get_by_id(data["location_id"]):
                raise ValueError("Location not found")

        if len(data["title"]) < 3:
            raise ValueError("Title too short")

        return await self.repo.create(data)

    async def update_post(self, post_id: int, data: dict):

        if not await self.user_repo.get_by_id(data["author_id"]):
            raise ValueError("Author not found")

        if data.get("category_id"):
            if not await self.category_repo.get_by_id(data["category_id"]):
                raise ValueError("Category not found")

        if data.get("location_id"):
            if not await self.location_repo.get_by_id(data["location_id"]):
                raise ValueError("Location not found")

        if len(data["title"]) < 3:
            raise ValueError("Title too short")
    
        return await self.repo.update(post_id, data)

    async def delete_post(self, post_id: int):
        return await self.repo.delete(post_id)
