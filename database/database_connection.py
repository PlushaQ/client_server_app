import psycopg2
from dotenv import dotenv_values


class DatabaseConnectionContextManager:
    def __init__(self, db_info):
        self.connection = None
        self.db_info = dotenv_values(db_info)

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(**self.db_info)
        except psycopg2.Error:
            print("Error occurred while connecting to database. Please check configurations and try again.")
        else:
            return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

# The DatabaseConnection class is a context manager that provides a convenient way to handle database connections.
# It allows you to establish a connection to a PostgreSQL database and automatically handles cleanup operations,
# such as committing transactions and closing the connection, when you're done using it.


class DatabaseConnection:
    def __init__(self, db_info, connection_id=0):
        self.connection = None
        self.host = dotenv_values(db_info)
        self.active = False
        self.connection_id = connection_id

    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.db_info)
        except psycopg2.Error:
            print("Error occurred while connecting to database. Please check configurations and try again.")
        else:
            return self.connection


