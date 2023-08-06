import socket
import json
import datetime
import threading

from database.database import ClientServerDatabase
from utils.server_command_handler import ServerResponseHandler


class ClientThread(threading.Thread):
    def __init__(self, conn, address, handler):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.handler = handler

    def run(self):
        print(f'Connected by {self.address}')

        try:
            while True:
                msg = self.conn.recv(1024).decode('utf8')
                if not msg:
                    break

                msg = json.loads(msg)
                command = msg['command'].split()

                if command and command[0] == 'stop':
                    self.conn.send(json.dumps({'message': 'stop'}).encode('utf-8'))
                    print(f'Shutting down a server')
                    break
                else:
                    self.conn.send(
                        json.dumps(
                            self.handler.handle_commands(command),
                            indent=4).encode('utf-8'))
        except Exception as e:
            print(f"Exception in client thread: {e}")
        finally:
            self.conn.close()


class Server:
    def __init__(self, host, port, database='database.env'):
        self.address = (host, port)
        self.server_start_time = datetime.datetime.now()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen()

        print(f"Listening on {self.address}")
        self.db = ClientServerDatabase(database)
        self.handler = ServerResponseHandler(self.server_start_time)
        self.client_threads = []  # List to store active client threads
        self.server_run = True

    def run(self):
        # Accept incoming connections
        while self.server_run:
            conn, addr = self.socket.accept()
            print(conn, addr)

            # Create new thread for each client
            client_thread = ClientThread(conn, addr, self.handler)
            self.client_threads.append(client_thread)
            client_thread.start()

    def stop(self):
        # Close all client threads gracefully
        self.db.db_conn_pool.run = False
        self.server_run = False
        for thread in self.client_threads:
            thread.join()  # Wait for each thread to finish
        self.db.close_connections()
        self.socket.close()


if __name__ == '__main__':
    server = Server('127.0.0.1', 64321)
    server.run()
