from datetime import datetime
from typing import Optional
import logging
from pydantic import computed_field

from pydantic import BaseModel, ConfigDict, field_validator

logger = logging.getLogger(__name__)


class PostBaseSchema(BaseModel):
    title: str
    text: str
    is_published: bool = True

    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str):
        if not v or not v.strip():
            logger.error("Validation failed for post title: empty")
            raise ValueError("Title cannot be empty")
        if len(v.strip()) < 3:
            logger.error("Validation failed for post title: too short")
            raise ValueError("Title must be at least 3 characters")
        return v.strip()

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str):
        if not v or not v.strip():
            logger.error("Validation failed for post text: empty")
            raise ValueError("Text cannot be empty")
        return v.strip()


class PostCreateSchema(PostBaseSchema):
    pass


class PostUpdateSchema(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    is_published: Optional[bool] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if v is None:
            return v
        if len(v.strip()) < 3:
            logger.error("Validation failed for post update title")
            raise ValueError("Title must be at least 3 characters")
        return v.strip()

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        if v is None:
            return v
        if not v.strip():
            logger.error("Validation failed for post update text")
            raise ValueError("Text cannot be empty")
        return v.strip()


class PostResponseSchema(PostBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    pub_date: Optional[datetime]
    created_at: datetime
    likes: int = 0
    dislikes: int = 0
