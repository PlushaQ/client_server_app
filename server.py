import socket
import json
import datetime


class Server:
    def __init__(self, host, port):
        self.address = (host, port)
        self.server_start_time = datetime.datetime.now()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen()
        print(f"Listening on {self.address}")

    def available_commands(self):
        commands = {
            'uptime': "returns the uptime of the server",
            'info': "returns version of server and it's date creation",
            'help': "show list of commands",
            'stop': "stops server and client",
        }
        return {'message': commands}

    def uptime(self):
        uptime = {"uptime": str(datetime.datetime.now() - self.server_start_time)}
        return {'message': uptime}

    @property
    def info(self):
        info = {
            'Version': '1.0.0',
            'Creation_date': str(self.server_start_time),
        }
        return {'message': info}

    def run(self):
        conn, addr = self.socket.accept()
        print(f'Connected by {addr}')
        while True:
            msg = conn.recv(1024).decode('utf8')
            if not msg:
                break
            
            msg = json.loads(msg)
            command = msg['command']
            print(f'Client send command - {command}')
            if command == 'uptime':
                conn.send(json.dumps(self.uptime()).encode('utf8'))
                print(f'Sending uptime to client ')

            elif command == 'info':
                conn.send(json.dumps(self.info).encode('utf8'))
                print(f'Sending server info to client ')

            elif command == 'help':
                conn.send(json.dumps(self.available_commands()).encode('utf8'))
                print(f'Sending command list to client ')

            elif command == 'stop':
                conn.send(json.dumps({'message': 'stop'}).encode('utf8'))
                print(f'Shutting down a server')
                self.socket.close()
                break
            else:
                conn.send(json.dumps({'message': 'Unknown command'}).encode('utf8'))
                print('Sending "Unknown command" to client')


if __name__ == '__main__':
    server = Server('127.0.0.1', 64321)
    server.run()