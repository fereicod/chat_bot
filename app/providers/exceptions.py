from typing import Any


class BaseException(Exception):
    default_message = "An error occurred in provider"

    def __init__(self, message: str, *args: Any) -> None:
        self.message = message or self.default_message
        super().__init__(self.message, *args)

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]: {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message='{self.message}')"


class DatabaseOperationError(BaseException):
    default_message = "Database operation failed"


class EntityCreationError(BaseException):
    default_message = "Failed to create entity"


class EntityNotFoundError(BaseException):
    default_message = "Entity not found"


class EntityFetchError(BaseException):
    default_message = "Failed to fetch entity data"