from functools import wraps
from typing import Any, Callable
from sqlalchemy.exc import SQLAlchemyError
from app.providers.exceptions import DatabaseOperationError
from app.core.logger import logger

def handle_db_operation():
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            try:
                return func(self, *args, **kwargs)
            except SQLAlchemyError as e:
                message = f"Database operation failed in {func.__name__}"
                logger.error(message, exc_info=True)
                raise DatabaseOperationError(message)
        return wrapper
    return decorator