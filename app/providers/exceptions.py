from typing import Any

class BaseException(Exception):
    def __init__(self, message: str, *args: Any) -> None:
        self.message = message
        super().__init__(self.message, *args)

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]: {self.message}"


class DatabaseOperationError(BaseException):
    pass