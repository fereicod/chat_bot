from sqlmodel import create_engine, Session
from app.database.base import DatabaseHandler
from app.database.database_config import DatabaseConfig

class MySQLHandler(DatabaseHandler):
    
    def create_engine(self, config: DatabaseConfig):
        url = config.get_database_url()
        return create_engine(
            url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=10,
            max_overflow=20
        )
    
    def get_session(self, engine) -> Session:
        return Session(engine)
