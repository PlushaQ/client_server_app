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

        while True:
            msg = self.conn.recv(1024).decode('utf8')
            if not msg:
                break

            msg = json.loads(msg)
            command = msg['command'].split()

            if command and command[0] == 'stop':
                self.conn.send(json.dumps({'message': 'stop'}).encode('utf-8'))
                print(f'Shutting down a server')
                self.conn.close()
                break
            else:
                self.conn.send(json.dumps(self.handler.handle_commands(command), indent=4).encode('utf-8'))


class Server:
    def __init__(self, host, port):
        self.address = (host, port)
        self.server_start_time = datetime.datetime.now()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen()
        print(f"Listening on {self.address}")
        self.db = ClientServerDatabase('database.env')
        self.handler = ServerResponseHandler(self.server_start_time)

    def run(self):
        # Accept incoming connections
        while True:
            conn, addr = self.socket.accept()

            # Create new thread for each client
            client_thread = ClientThread(conn, addr, self.handler)
            client_thread.start()


if __name__ == '__main__':
    server = Server('127.0.0.1', 64322)
    server.run()
