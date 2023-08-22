import psycopg2
import sqlite3
from dotenv import dotenv_values


class DatabaseConnection:
    def __init__(self, db_info):
        self.connection = None
        self.db_info = dotenv_values(db_info)
        self.active = False
        self.connection_id = None

    def __repr__(self):
        return f'<Connection ID {self.connection_id}. Active: {self.active}>'

    def _connect(self):
        if len(self.db_info) == 1:
            try:
                self.connection = sqlite3.connect(self.db_info['database'])
            except sqlite3.Error:
                print("Error occurred while connecting to SQLITE database. Please check configurations and try again.")
        else:
            try:
                self.connection = psycopg2.connect(**self.db_info)
            except psycopg2.Error:
                print("Error occurred while connecting to postgre database. Please check configurations and try again.")

        self.connection_id = id(self.connection)

    def conn_info(self):
        self._connect()
        return self


# class DatabaseContextManager:
#     def __init__(self, pool):
#         self.pool = pool
#         self.connection = None
#         self.cursor = None
#
#     def _get_conn(self):
#         return self.pool.start_new_connection()
#
#     def __enter__(self):
#         self.connection = self._get_conn()
#         if self.connection is None:
#             time.sleep(2)
#             return self._get_conn()
#         self.cursor = self.connection.cursor()
#         return self.connection, self.cursor
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.cursor.close()
#         self.connection.commit()
#         self.pool.return_connection_to_pool(self.connection)
#
