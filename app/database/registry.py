from app.database.adapters.mysql_adapter import MySQLHandler

DATABASE_REGISTRY = {
    "mysql": {
        "name": "MySQL",
        "handler": MySQLHandler,
    },
}
