import psycopg2
from dotenv import dotenv_values
from database_connection import DatabaseConnection


class ClientServerDatabase:
    def __init__(self):
        host_info = dotenv_values('database.env')
        with DatabaseConnection(host_info) as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            username VARCHAR(255) PRIMARY KEY,
                            password VARCHAR(255),
                            role VARCHAR(5)
                            )''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                            username VARCHAR(255) REFERENCES users (username),
                            message_id INTEGER,
                            sender VARCHAR(255),
                            time TIMESTAMP,
                            body TEXT,
                            is_read BOOLEAN,
                            PRIMARY KEY (username, message_id)
            )''')
            cursor.close()


db = ClientServerDatabase()