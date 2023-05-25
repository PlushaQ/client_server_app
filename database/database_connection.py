import psycopg2
from dotenv import dotenv_values


class DatabaseConnection:
    def __init__(self, host):
        self.connection = None
        self.host = dotenv_values(host)

    def __enter__(self):
        self.connection = psycopg2.connect(**self.host)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

