from typing import Any


class BaseException(Exception):
    default_message = "An error occurred in the service"

    def __init__(self, message: str, *args: Any) -> None:
        self.message = message or self.default_message
        super().__init__(self.message, *args)

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]: {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message='{self.message}')"


class ChatServiceError(BaseException):
    default_message = "Chat service operation failed"


class ConversationError(BaseException):
    default_message = "Conversation operation failed"


class MessageError(BaseException):
    default_message = "Message operation failed"
