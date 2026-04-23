from pydantic import (BaseModel, ConfigDict, SecretStr, EmailStr,
                      field_validator)
from typing import Optional
import logging

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
    def validate_username(cls, v):
        if len(v.strip()) < 3:
            logger.error("Validation failed for username: '%s'", v)
            raise ValueError("Username too short")
        logger.info("Validated username: %s", v)
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v.get_secret_value()) < 6:
            logger.error("Validation failed for password: too short")
            raise ValueError("Password too short")
        logger.info("Validated password for user")
        return v


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_superuser: bool

    @field_validator("email", mode="before")
    @classmethod
    def empty_email_to_none(cls, v):
        if v == "":
            logger.info("Email empty, converting to None")
            return None
        return v