from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
import logging

logger = logging.getLogger(__name__)

class CategorySchema(BaseModel):
    """Класс категорий."""

    model_config = ConfigDict(from_attributes=True)
    title: str
    description: str
    slug: str
    created_at: datetime
    is_published: int

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v):
        if not v or len(v.strip()) == 0:
            logger.error("Validation failed for slug: empty value")
            raise ValueError("Slug cannot be empty")
        logger.info("Validated slug: %s", v)
        return v