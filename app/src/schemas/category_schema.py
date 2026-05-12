from datetime import datetime
from typing import Optional
import logging

from pydantic import BaseModel, ConfigDict, field_validator

logger = logging.getLogger(__name__)


class CategoryBaseSchema(BaseModel):
    title: str
    description: Optional[str] = None
    slug: str
    is_published: bool = True

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str):
        if not v or not v.strip():
            logger.error("Validation failed for slug: empty value")
            raise ValueError("Slug cannot be empty")
        return v.strip()


class CategoryCreateSchema(CategoryBaseSchema):
    pass


class CategoryUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    is_published: Optional[bool] = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v):
        if v is not None and not v.strip():
            logger.error("Validation failed for slug: empty value")
            raise ValueError("Slug cannot be empty")
        return v.strip()


class CategoryResponseSchema(CategoryBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime