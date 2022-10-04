import os
from sqlalchemy import create_engine
from utils import Logger, Singleton


DSN_CONSTANT = "{}+mysqlconnector://{}:{}@{}:{}/{}"


class DBConnector(metaclass=Singleton):
    """create a singleton connection pool with the database 

        Args:
            metaclass (_type, optional): _description_. Defaults to Singleton
    """

    def __init__(self) -> None:
        """Initialize"""
        user_name = os.getenv("DB_USERNAME")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        dbname = os.getenv("DB_NAME")
        dialect = os.getenv("DB_DIALECT")

        self.engine = None
        self.dsn = DSN_CONSTANT.format(
            dialect, user_name, password, host, port, dbname)
        self.logger = Logger().get_logger()

    def connect(self):
        """"create a connection pool with the database"""
        try:
            self.logger.debug("Creating a DB engine")
            if self.engine is None:
                self.engine = create_engine(
                    self.dsn, pool_size=100, max_overflow=0)
            self.logger.info("Connected to sql server ✔️")
        except Exception as ex:
            self.logger.debug(f"Failed to create a DB engine, {str(ex)}")

    def get_engine(self):
        """Get the database engine.
        Returns:
            Engine: Database engine.
        """
        return self.engine

    def dispose_connection(self):
        """Close the Database connection pool."""
        self.engine.dispose(True)

    def get_connection_string(self):
        """returns the connection string to the database"""
        return self.dsn
