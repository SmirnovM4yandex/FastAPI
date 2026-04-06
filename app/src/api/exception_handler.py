from fastapi import HTTPException
from src.core.exceptions.exceptions import (
    AppException,
    NotFoundException,
    ConflictException,
    ValidationException,
    DatabaseException
)


def handle_exception(ex: Exception):
    if isinstance(ex, AppException):
        ex.log()

        if isinstance(ex, NotFoundException):
            raise HTTPException(404, ex.message)

        if isinstance(ex, ConflictException):
            raise HTTPException(409, ex.message)

        if isinstance(ex, ValidationException):
            raise HTTPException(400, ex.message)

        if isinstance(ex, DatabaseException):
            raise HTTPException(500, "Internal database error")

    raise ex