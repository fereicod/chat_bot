from abc import ABC, abstractmethod
from sqlmodel import Session
from app.database.database_config import DatabaseConfig

class DatabaseHandler(ABC):    
    @abstractmethod
    def create_engine(self, config: DatabaseConfig):
        pass
    
    @abstractmethod
    def get_session(self, engine) -> Session:
        pass
