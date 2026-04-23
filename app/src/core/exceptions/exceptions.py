from typing import Optional, Any, Dict
from src.core.exceptions.logger import logger


class AppException(Exception):

    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.details = details or {}
        super().__init__(message)

    def log(self):
        logger.error(
            f"{self.__class__.__name__}: {self.message} | {self.details}"
        )


class DatabaseException(AppException):

    def log(self):
        logger.exception(
            f"Database error: {self.message} | {self.details}"
        )


class NotFoundException(AppException):

    def log(self):
        logger.warning(
            f"Not found: {self.message} | {self.details}"
        )


class ConflictException(AppException):

    def log(self):
        logger.warning(
            f"Conflict: {self.message} | {self.details}"
        )


class ValidationException(AppException):

    def log(self):
        logger.warning(
            f"Validation error: {self.message} | {self.details}"
        )

class WrongPasswordException(AppException):

    def log(self):
        logger.warning(
            f"Wrong password: {self.message} | {self.details}"
        )