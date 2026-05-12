from datetime import datetime
from typing import Optional
import logging

from pydantic import BaseModel, ConfigDict, field_validator

logger = logging.getLogger(__name__)


class LocationBaseSchema(BaseModel):
    name: str
    is_published: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str):
        if not v or not v.strip():
            logger.error("Validation failed for location name")
            raise ValueError("Location name cannot be empty")
        return v.strip()


class LocationCreateSchema(LocationBaseSchema):
    pass


class LocationUpdateSchema(BaseModel):
    name: Optional[str] = None
    is_published: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if v is not None and not v.strip():
            logger.error("Validation failed for location name")
            raise ValueError("Location name cannot be empty")
        return v.strip() if v else v


class LocationResponseSchema(LocationBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime