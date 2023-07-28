import threading
import time

from .database_connection import DatabaseConnection


class DatabaseConnectionPoolManager:
    def __init__(self, database_info, time_limit=None):
        self.db_info = database_info
        self.starting_conns = 5
        self.max_connections = 50

        self.connections = [DatabaseConnection(self.db_info).conn_info() for _ in range(self.starting_conns)]

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
            return None
        if len(inactive_conns) == 0:
            with self.semaphore:
                new_conn = DatabaseConnection(self.db_info).conn_info()
                new_conn.active = True
                self.connections.append(new_conn)

                return new_conn.connection
        with self.semaphore:
            new_conn = inactive_conns[0]
            new_conn.active = True

            return new_conn.connection

    def return_connection_to_pool(self, conn):
        conn = [x for x in self.connections if x.connection is conn]
        if conn:
            with self.semaphore:
                conn[0].active = False
                self.connections_realised += 1

    def close_all_connections(self):
        with self.semaphore:
            self.run = False
            for conn in self.connections:
                conn.connection.close()
            self.connections.clear()

    def _connection_loop(self):
        while self.run:
            inactive_conns = [conn for conn in self.connections if not conn.active]
            connections_to_remove = inactive_conns[4:]
            with self.semaphore:
                for conn in connections_to_remove:
                    conn.connection.close()
                    self.connections.remove(conn)

            print(f"""Time from start: {round(time.time() - self.initialization_time, 2)}
Realised connections: {self.connections_realised}
Active connections: {len(self.connections)}
Connections: {','.join([str(x.connection_id) for x in self.connections])}
""")

            time.sleep(10)

            if self.time_limit:
                self.working_time = time.time() - self.initialization_time
                if self.time_limit < self.working_time:
                    self.run = False
                    break
