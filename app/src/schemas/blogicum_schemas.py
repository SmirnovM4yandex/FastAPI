"""Представления моделей приложения."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, SecretStr, EmailStr
from typing import Optional


class CategorySchema(BaseModel):
    """Класс категорий."""

    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    slug: str


class LocationSchema(BaseModel):
    """Класс локации."""

    model_config = ConfigDict(from_attributes=True)
    name: str


class PostSchema(BaseModel):
    """Класс поста."""

    model_config = ConfigDict(from_attributes=True)
    title: str
    text: str
    pub_date: datetime
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None


class CommentSchema(BaseModel):
    """Класс комментария."""

    model_config = ConfigDict(from_attributes=True)
    post_id: int
    author_id: int
    text: str


class User(BaseModel):
    """Класс польователя."""

    username: str
    email: EmailStr
    password: SecretStr
    first_name: Optional[str] = None
    second_name: Optional[str] = None
