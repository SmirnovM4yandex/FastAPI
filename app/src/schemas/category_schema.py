from datetime import datetime
import logging

from pydantic import BaseModel, ConfigDict, field_validator

logger = logging.getLogger(__name__)


class CategoryBaseSchema(BaseModel):
    title: str
    description: str
    slug: str
    is_published: bool = True

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v):
        if not v or len(v.strip()) == 0:
            logger.error("Validation failed for slug: empty value")
            raise ValueError("Slug cannot be empty")
        return v


class CategoryCreateSchema(CategoryBaseSchema):
    pass


class CategoryResponseSchema(CategoryBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime