"""Представления моделей приложения."""
from datetime import datetime
from pydantic import (BaseModel, ConfigDict, SecretStr, EmailStr,
                      field_validator)
from typing import Optional


class CategorySchema(BaseModel):
    """Класс категорий."""

    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    slug: str
    created_at: datetime
    is_published: int


class LocationSchema(BaseModel):
    """Класс локации."""

    model_config = ConfigDict(from_attributes=True)
    name: str
    is_published: int
    created_at: datetime


class PostSchema(BaseModel):
    """Класс поста."""

    model_config = ConfigDict(from_attributes=True)
    title: str
    text: str
    pub_date: datetime
    created_at: datetime
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None
    is_published: bool


class CommentSchema(BaseModel):
    """Класс комментария."""

    model_config = ConfigDict(from_attributes=True)
    post_id: int
    author_id: int
    text: str
    created_at: datetime


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator("email", mode="before")
    @classmethod
    def empty_email_to_none(cls, v):
        if v == "":
            return None
        return v
