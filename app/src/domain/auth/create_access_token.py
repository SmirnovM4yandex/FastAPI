from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "STRONG_SECRET_KEY"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60


class CreateAccessTokenUseCase:

    async def execute(self, login: str) -> str:
        payload = {
            "sub": login,
            "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)