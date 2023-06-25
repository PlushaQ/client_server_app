import threading
import time


from .database_connection import DatabaseConnectionContextManager as DatabaseConnection


class DatabaseConnectionPoolManager:
    def __init__(self, database_info):
        self.db_info = database_info
        self.starting_conns = 5
        self.max_connections = 50

        self.connections = [DatabaseConnection(self.db_info, i).conn_info() for i in range(self.starting_conns)]
        self.initialization_time = time.time()

        self.semaphore = threading.Semaphore(self.max_connections)

        self.thread = threading.Thread(target=self._connection_loop)
        self.thread.start()

    def start_new_connection(self):
        with self.semaphore:
            inactive_conns = [conn for conn in self.connections if conn.active is False]
            if len(inactive_conns) == 0:
                new_conn = DatabaseConnection(self.db_info, len(self.connections)).conn_info()
                new_conn.active = True
                self.connections.append(new_conn)
                print(f"Connected to database. Connection id = {new_conn.connection_id}")
                return new_conn
            if len(self.connections) >= self.max_connections:
                print("Reached maximum connections. Please try again later")
                return None

            new_conn = inactive_conns[0]
            new_conn.active = True
            print(f"Connected to database. Connection id = {new_conn.connection_id}")
            return new_conn

    def return_connection_to_pool(self, conn):
        with self.semaphore:
            conn.active = False
            if conn.connection_id < 5:
                self.connections.remove(conn)

    def close_all_connections(self):
        with self.semaphore:
            for conn in self.connections:
                conn.connection.close()
            self.connections.clear()

    def _connection_loop(self):
        while True:
            with self.semaphore:
                inactive_conns = [conn for conn in self.connections if conn.active is False]
                if len(inactive_conns) > 0:
                    for conn in inactive_conns:
                        print(conn.connection_id )
                        if conn.connection_id > 4:
                            self.connections.remove(conn)
                print(f"""
Conns: {len(self.connections)}
Time from start: {round(time.time() - self.initialization_time, 2)}
""")
                time.sleep(2)
