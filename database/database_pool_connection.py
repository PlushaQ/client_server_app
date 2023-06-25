import threading
import time


from database_connection import DatabaseConnection


class DatabaseConnectionManager:
    def __init__(self, database_info):
        self.database_info = database_info
        self.starting_connections = 5
        self.max_connections = 50

        self.initialization_time = time.time()
        self.connections = [DatabaseConnection(database_info, i).connect() for i in range(self.starting_connections)]

        self.semaphore = threading.Semaphore(self.max_connections)

    def start_new_connection(self):
        pass

    def return_connection_to_pool(self):
        pass

    def kill_all_connections(self):
        pass

