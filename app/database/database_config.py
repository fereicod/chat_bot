from app.core.config import settings

class DatabaseConfig:
    
    def __init__(self):
        self.db_type = self._detect_database_type()
        self.connection_params = self._get_connection_params()
    
    def _detect_database_type(self) -> str:
        # INFO: Avoid circular import
        from app.database.registry import DATABASE_REGISTRY

        db_type = settings.DB_TYPE
        if db_type and db_type in DATABASE_REGISTRY:
            return db_type
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    
    def _get_connection_params(self) -> dict:
        if self.db_type == "mysql":
            return {
                "host": settings.MYSQL_HOST,
                "user": settings.MYSQL_USER,
                "password": settings.MYSQL_PASSWORD,
                "database": settings.MYSQL_DATABASE,
                "port": settings.MYSQL_PORT
            }
        
        return {}
    
    def get_database_url(self) -> str:
        if self.db_type == "mysql":
            params = self.connection_params
            return f"mysql+pymysql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
        
        raise ValueError(f"Unsupported database type: {self.db_type}")
