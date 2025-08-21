from functools import wraps
from typing import Any, Callable, Type, Optional
from sqlalchemy.exc import SQLAlchemyError
from app.providers.exceptions import BaseException, DatabaseOperationError
from app.core.logger import logger

def handle_db_operation(error_to_raise: Type[BaseException] = DatabaseOperationError, messsage: Optional[str] = None):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            try:
                return func(self, *args, **kwargs)
            
            except SQLAlchemyError as e:
                self.session.rollback()
                
                class_name = self.__class__.__name__ if hasattr(self, "__class__") else ""
                func_location = f"{class_name}.{func.__name__}" if class_name else func.__name__

                if messsage:
                    logger.error(f"{messsage} in {func_location}: {e}", exc_info=True)
                    raise error_to_raise(messsage)
                
                error_msg = messsage or f"Database operation failed in {func_location}: {e}"
                logger.error(error_msg, exc_info=True)
                raise error_to_raise(error_msg)
            
        return wrapper
    return decorator