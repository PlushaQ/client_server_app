import socket
import json
import datetime

from users import User


class Server:
    def __init__(self, host, port):
        self.address = (host, port)
        self.server_start_time = datetime.datetime.now()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen()
        print(f"Listening on {self.address}")
        self.user = User()

    def available_commands_before_login(self):
        commands = {
            'uptime': "returns the uptime of the server",
            'info': "returns version of server and it's date creation",
            'help': "show list of commands",
            'stop': "stops server and client",
            'register': 'registers new users. usage: <register username password>',
            'login': 'log in user. usage: <login username password>'

        }
        return {'message': commands}

    def available_commands_after_login(self):
        commands = {
            'uptime': "returns the uptime of the server",
            'info': "returns version of server and it's date creation",
            'help': "show list of commands",
            'stop': "stops server and client",
            'register': 'registers new users. usage: <register username password>',
            'login': 'log in user. usage: <login username password>',
            'send': 'send user a message. usage <send user message(max. 255 chars)>',
            'unread': 'shows unread messages from users inbox. usage <unread username>',
            'inbox': 'shows users inbox. usage: <inbox username>',
            'user_list': 'shows users in the server'  
        }
        return {'message': commands}

    @property
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
            command = msg['command'].split()
            print(f'Client send command - {command}')
            if not command:
                conn.send(json.dumps({'message': 'No command provided'}).encode('utf8'))
                print('Sending "No command provided" to client')

            elif command[0] == 'uptime':
                conn.send(json.dumps(self.uptime).encode('utf8'))
                print(f'Sending uptime to client ')

            elif command[0] == 'info':
                conn.send(json.dumps(self.info).encode('utf8'))
                print(f'Sending server info to client ')

            elif command[0] == 'help':
                if self.user.username is None:
                    conn.send(json.dumps(self.available_commands_before_login()).encode('utf-8'))
                else:
                    conn.send(json.dumps(self.available_commands_after_login()).encode('utf-8'))
                print(f'Sending command list to client ')
            
            elif command[0] == 'register':
                if len(command) != 3:
                    conn.send(json.dumps({'message': {'Usage': '<register username password>'}}).encode('utf-8'))
                else:
                    conn.send(self.user.register_user(command[1], command[2]).encode('utf-8'))

            elif command[0] == 'login':
                if len(command) != 3:
                    conn.send(json.dumps({'message': {'Usage': '<login username password>'}}).encode('utf-8'))
                else:
                    conn.send(self.user.login_user(command[1], command[2]).encode('utf-8'))
                    print(f"Logged {self.user.username} with role {self.user.role}")
            
            elif command[0] == 'user_list':
                conn.send(self.user.user_list().encode('utf-8'))
                print('Sending to client user list')

            elif command[0] == 'send':
                conn.send(self.user.send_message(command[1], ' '.join(command[2:]), self.user.username).encode('utf-8'))
                print(f'Sending messages from {self.user.username} to {command[1]}')
            
            elif command[0] == 'inbox':
                conn.send(self.user.show_inbox(command[1]).encode('utf8'))
                print(f'Showing {command[1]} inbox.')
                          

            elif command[0] == 'stop':
                conn.send(json.dumps({'message': 'stop'}).encode('utf8'))
                print(f'Shutting down a server')
                self.socket.close()
                break
            else:
                conn.send(json.dumps({'message': 'Unknown command'}).encode('utf8'))
                print('Sending "Unknown command" to client')


if __name__ == '__main__':
    server = Server('127.0.0.1', 64322)
    server.run()