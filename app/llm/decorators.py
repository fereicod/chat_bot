from functools import wraps
from typing import Any, Callable, Type, Optional
from app.core.logger import logger
from app.llm.exceptions import BaseException, LLMServiceError, GeminiServiceError

def handle_gemini_errors(
    error_to_raise: Type[BaseException] = LLMServiceError,
    message: Optional[str] = None
):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            try:
                return func(self, *args, **kwargs)

            except GeminiServiceError as e:
                error_msg = "Gemini API error"
                _log_and_raise_gemini_error(self, func, e, error_to_raise, message, error_msg)

            except LLMServiceError as e:
                error_msg = "Gemini service error"
                _log_and_raise_gemini_error(self, func, e, error_to_raise, message, error_msg)
            
            except Exception as e:
                error_msg = "Unexpected Gemini error"
                _log_and_raise_gemini_error(self, func, e, error_to_raise, message, error_msg)
            
        return wrapper
    return decorator

def _log_and_raise_gemini_error(
    self: Any,
    func: Callable,
    original_error: Exception,
    error_to_raise: Type[BaseException],
    custom_message: Optional[str],
    error_type: str
) -> None:
    class_name = self.__class__.__name__ if hasattr(self, "__class__") else ""
    func_location = f"{class_name}.{func.__name__}" if class_name else func.__name__
    
    if custom_message:
        logger.error(f"{custom_message} in {func_location}: {original_error}", exc_info=True)
        raise error_to_raise(custom_message)
    
    full_error_msg = f"{error_type} in {func_location}: {original_error}"
    logger.error(full_error_msg, exc_info=True)
    raise error_to_raise(full_error_msg)