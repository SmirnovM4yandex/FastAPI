from datetime import datetime
import logging

from pydantic import BaseModel, ConfigDict, field_validator

logger = logging.getLogger(__name__)


class CommentBaseSchema(BaseModel):
    post_id: int
    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        if not v or len(v.strip()) == 0:
            logger.error("Validation failed for comment text")
            raise ValueError("Comment text cannot be empty")
        return v


class CommentCreateSchema(CommentBaseSchema):
    pass


class CommentResponseSchema(CommentBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    created_at: datetime