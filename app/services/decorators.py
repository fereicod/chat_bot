from functools import wraps
from typing import Any, Callable, Type, Optional
from app.providers.exceptions import BaseException as ProviderBaseException
from app.services.exceptions import (
    BaseException,
    ChatServiceError,
    ConversationError,
    MessageError
)
from app.core.logger import logger

def handle_service_errors(
    error_to_raise: Type[BaseException] = ChatServiceError, 
    message: Optional[str] = None
):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            try:
                return func(self, *args, **kwargs)
            
            except (ConversationError, MessageError) as e:
                error_msg = "Services logic error"
                _log_and_raise_error(self, func, e, error_to_raise, message, error_msg)
            
            except ProviderBaseException as e:
                error_msg = "Provider error"
                _log_and_raise_error(self, func, e, error_to_raise, message, error_msg)
            
            except Exception as e:
                error_msg = "Unexpected error"
                _log_and_raise_error(self, func, e, error_to_raise, message, error_msg)
            
        return wrapper
    return decorator

def _log_and_raise_error(
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