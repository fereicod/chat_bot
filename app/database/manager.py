from sqlmodel import Session
from app.database.database_config import DatabaseConfig
from app.database.factory import DatabaseHandlerFactory


class DatabaseManager:    
    _instance = None
    _config = None
    _engine = None
    _handler = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._initialize_database()
    
    def _initialize_database(self):
        try:
            self._config = DatabaseConfig()
            self._handler = DatabaseHandlerFactory.create_handler(self._config.db_type)
            self._engine = self._handler.create_engine(self._config)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize database: {e}")
    
    def get_engine(self):
        return self._engine
    
    def get_session(self) -> Session:
        if self._handler is None or self._engine is None:
            raise RuntimeError("Database handler or engine is not initialized.")
        return self._handler.get_session(self._engine)
    
    def close_connection(self):
        if self._engine:
            self._engine.dispose()

def get_session():
    session = DatabaseManager().get_session()
    try:
        yield session
    finally:
        session.close()


