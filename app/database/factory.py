from app.database.base import DatabaseHandler
from app.database.registry import DATABASE_REGISTRY

class DatabaseHandlerFactory:

    @classmethod
    def create_handler(cls, db_type: str) -> DatabaseHandler:
        if db_type not in DATABASE_REGISTRY:
            raise ValueError(f"Unsupported database type: {db_type}")
        return DATABASE_REGISTRY[db_type]["handler"]() # type: ignore
