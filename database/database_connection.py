import psycopg2
from dotenv import dotenv_values
import time


class DatabaseConnection:
    def __init__(self, db_info, connection_id):
        self.connection = None
        self.db_info = dotenv_values(db_info)
        self.active = False
        self.connection_id = connection_id

    def __repr__(self):
        return f'<Connection ID {self.connection_id}. Active: {self.active}>'

    def _connect(self):
        try:
            self.connection = psycopg2.connect(**self.db_info)
        except psycopg2.Error:
            print("Error occurred while connecting to database. Please check configurations and try again.")

    def conn_info(self):
        self._connect()
        return self


class DatabaseContextManager:
    def __init__(self, pool):
        self.pool = pool
        self.connection = None

    def __enter__(self):
        self.connection = self.pool.start_new_connection()
        while self.connection is None:
            time.sleep(2)
            self.connection = self.pool.start_new_connection()
        return self.connection.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.connection.commit()
        self.pool.return_connection_to_pool(self.connection)

# The DatabaseConnection class is a context manager that provides a convenient way to handle database connections.
# It allows you to establish a connection to a PostgreSQL database and automatically handles cleanup operations,
# such as committing transactions and closing the connection, when you're done using it.


