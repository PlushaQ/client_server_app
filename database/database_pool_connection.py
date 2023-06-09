import threading
import time


from .database_connection import DatabaseConnection


class DatabaseConnectionPoolManager:
    def __init__(self, database_info, time_limit=None):
        self.db_info = database_info
        self.starting_conns = 5
        self.max_connections = 50

        self.connections = [DatabaseConnection(self.db_info, x).conn_info() for x in range(self.starting_conns)]

        self.initialization_time = time.time()
        self.working_time = self.initialization_time
        self.time_limit = time_limit

        self.connections_realised = 0

        self.run = True

        self.semaphore = threading.Semaphore(self.max_connections)

        self.thread = threading.Thread(target=self._connection_loop)
        self.thread.start()

    def start_new_connection(self):

        inactive_conns = [conn for conn in self.connections if conn.active is False]
        if len(self.connections) >= self.max_connections and len(inactive_conns) == 0:
            # print("Reached maximum connections. Please try again later")
            return None
        if len(inactive_conns) == 0:
            with self.semaphore:
                new_conn = DatabaseConnection(self.db_info, len(self.connections)).conn_info()
                new_conn.active = True
                self.connections.append(new_conn)
                # print(f"Connected to database. Connection id = {new_conn.connection_id}")
                return new_conn
        with self.semaphore:
            new_conn = inactive_conns[0]
            new_conn.active = True
            # print(f"Connected to database. Connection id = {new_conn.connection_id}")
            return new_conn

    def return_connection_to_pool(self, conn):
        with self.semaphore:
            conn = [x for x in self.connections if x is conn]
            if conn:
                conn[0].active = False
                self.connections_realised += 1
                # print(f"Released connection ID: {conn[0].connection_id}")

    def close_all_connections(self):
        with self.semaphore:
            self.run = False
            for conn in self.connections:
                conn.connection.close()
            self.connections.clear()

    def _connection_loop(self):
        while self.run:
            with self.semaphore:
                inactive_conns = [conn for conn in self.connections if not conn.active]
                connections_to_remove = []
                for conn in inactive_conns:
                    print('realising')
                    if conn.connection_id > 4:
                        conn.connection.close()
                        connections_to_remove.append(conn)

                for conn in connections_to_remove:
                    self.connections.remove(conn)

            print(f"""Time from start: {round(time.time() - self.initialization_time, 2)}
Realised connections: {self.connections_realised}
Active connections: {len(self.connections)}
""")

            time.sleep(2)

            if self.time_limit:
                self.working_time = time.time() - self.initialization_time
                if self.time_limit < self.working_time:
                    self.run = False
                    break