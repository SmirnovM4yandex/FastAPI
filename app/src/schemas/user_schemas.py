from typing import Optional
import logging

from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr, field_validator

logger = logging.getLogger(__name__)


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_superuser: bool = False

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str):
        v = v.strip()
        if len(v) < 3:
            logger.error("Validation failed for username")
            raise ValueError("Username too short")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: SecretStr):
        if len(v.get_secret_value()) < 6:
            logger.error("Validation failed for password")
            raise ValueError("Password too short")
        return v


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if v is not None and len(v.strip()) < 3:
            logger.error("Validation failed for username")
            raise ValueError("Username too short")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if v is not None and len(v.get_secret_value()) < 6:
            logger.error("Validation failed for password")
            raise ValueError("Password too short")
        return v


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]

    is_superuser: bool
    is_staff: bool
    is_active: bool
