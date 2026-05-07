from datetime import datetime
from typing import Optional
import logging

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
    def validate_title(cls, v):
        if not v or len(v.strip()) < 3:
            logger.error("Validation failed for post title")
            raise ValueError("Title must be at least 3 characters")
        return v


class PostCreateSchema(PostBaseSchema):
    pass


class PostResponseSchema(PostBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    pub_date: datetime
    created_at: datetime