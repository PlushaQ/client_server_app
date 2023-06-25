import threading
import time


from database_connection import DatabaseConnection


class DatabaseConnectionPoolManager:
    def __init__(self, database_info):
        self.db_info = database_info
        self.starting_conns = 5
        self.max_connections = 50

        self.connections = [DatabaseConnection(self.db_info, i).conn_info() for i in range(self.starting_conns)]
        self.initialization_time = time.time()
        print(self.connections)

        self.semaphore = threading.Semaphore(self.max_connections)

    def start_new_connection(self):
        inactive_conns = [conn for conn in self.connections if conn.active is False]
        if len(inactive_conns) == 0 and len(self.connections) >= self.max_connections:
            print("Reached maximum connections. Please try again later")
        elif len(inactive_conns) == 0:
            new_conn = DatabaseConnection(self.db_info, len(self.connections)).conn_info()
            new_conn.active = True
            self.connections.append(new_conn)
            print(f"Connected to database. Connection id = {new_conn.connection_id}")
            return new_conn
        else:
            new_conn = inactive_conns[0]
            new_conn.active = True
            print(f"Connected to database. Connection id = {new_conn.connection_id}")
            return new_conn

    def return_connection_to_pool(self):
        pass

    def kill_all_connections(self):
        for conn in self.connections:
            conn.connection.close()


db = DatabaseConnectionPoolManager('database.env')
db.start_new_connection()
print(db.connections)
db.kill_all_connections()
print(db.connections)
