from datetime import datetime
import logging
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

logger = logging.getLogger(__name__)


class CommentBaseSchema(BaseModel):
    post_id: int
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str):
        if not v or not v.strip():
            logger.error("Validation failed for comment text")
            raise ValueError("Comment text cannot be empty")
        return v.strip()


class CommentCreateSchema(CommentBaseSchema):
    pass


class CommentUpdateSchema(BaseModel):
    text: Optional[str] = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        if v is not None and not v.strip():
            logger.error("Validation failed for comment text")
            raise ValueError("Comment text cannot be empty")
        return v


class CommentResponseSchema(CommentBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    created_at: datetime