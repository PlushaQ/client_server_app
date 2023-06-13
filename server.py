import socket
import json
import datetime

from users.users import User
from utils.server_command_handler import ServerResponseHandler


class Server:
    def __init__(self, host, port):
        self.address = (host, port)
        self.server_start_time = datetime.datetime.now()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen()
        print(f"Listening on {self.address}")
        self.handler = ServerResponseHandler(self.server_start_time)

    def run(self):
        # Accept incoming connections
        conn, addr = self.socket.accept()
        print(f'Connected by {addr}')
        
        while True:
            # Receive command from the client
            msg = conn.recv(1024).decode('utf8')
            if not msg:
                break
            
            msg = json.loads(msg)
            command = msg['command'].split()
            

            if command and command[0] == 'stop':
                conn.send(json.dumps({'message': 'stop'}).encode('utf-8'))
                print(f'Shutting down a server')
                self.socket.close()
                break
            
            else:
                conn.send(json.dumps(self.handler.handle_commands(command), indent=4).encode('utf-8'))


if __name__ == '__main__':
    server = Server('127.0.0.1', 64322)
    server.run()