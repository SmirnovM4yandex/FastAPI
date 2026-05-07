from datetime import datetime, timedelta
from jose import jwt
from src.core.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


class CreateAccessTokenUseCase:

    async def execute(self, login: str) -> str:
        payload = {
            "sub": login,
            "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)