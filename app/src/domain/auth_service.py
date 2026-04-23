from typing import Annotated

from fastapi import Depends
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_db
from src.repositories.user_repository import UserRepository
from src.resources.auth import oauth2_scheme
from src.core.exceptions.auth_exceptions import CredentialsException

SECRET_KEY = "STRONG_SECRET_KEY"
ALGORITHM = "HS256"


class AuthService:
    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db),
    ):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            login: str = payload.get("sub")

            if login is None:
                raise CredentialsException("Invalid token")

        except JWTError:
            raise CredentialsException("Invalid token")

        repo = UserRepository(db)
        user = await repo.get_by_username(login)

        if not user:
            raise CredentialsException("User not found")

        return user