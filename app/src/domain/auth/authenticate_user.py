from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_repository import UserRepository
from src.resources.auth import verify_password
from src.core.exceptions.exceptions import NotFoundException, WrongPasswordException


class AuthenticateUserUseCase:

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def execute(self, login: str, password: str):
        user = await self.repo.get_by_username(login)

        if not user:
            raise NotFoundException("User not found", {"login": login})

        if not verify_password(password, user.password):
            raise WrongPasswordException("Invalid password")

        return user