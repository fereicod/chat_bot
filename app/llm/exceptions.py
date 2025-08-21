from typing import Any


class BaseException(Exception):
    default_message = "An error occurred in the system LLM"

    def __init__(self, message: str, *args: Any) -> None:
        self.message = message or self.default_message
        super().__init__(self.message, *args)

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]: {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message='{self.message}')"
    
class LLMServiceError(BaseException):
    default_message = "Language Model service operation failed"

class GeminiServiceError(LLMServiceError):
    default_message = "Gemini API operation failed"