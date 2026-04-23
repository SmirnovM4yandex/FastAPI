from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_db
from src.domain.auth.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.create_access_token import CreateAccessTokenUseCase


def authenticate_user_use_case(
    db: AsyncSession = Depends(get_db),
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(db)


def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()