import threading
import time
import psycopg2


class DatabaseConnectionManager:
    def __init__(self, database_info):
        self.database_info = database_info
        self.starting_connections = 5
        self.max_connections = 100

    def start_new_connection(self):
        pass

    def return_connection_to_pool(self):
        pass

    def kill_all_connections(self):
        pass