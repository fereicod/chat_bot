from functools import wraps
from typing import Any, Callable, Type
from sqlalchemy.exc import SQLAlchemyError
from app.providers.exceptions import DatabaseOperationError, BaseException
from app.core.logger import logger

def handle_db_operation(error_to_raise: Type[BaseException] = DatabaseOperationError):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            try:
                return func(self, *args, **kwargs)
            except SQLAlchemyError as e:
                self.session.rollback()
                message = f"Database operation failed in {func.__name__}"
                logger.error(f"{message}: {e}", exc_info=True)
                raise error_to_raise(message)
        return wrapper
    return decorator