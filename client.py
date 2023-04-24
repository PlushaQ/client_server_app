import socket
import json


class Client:
    def __init__(self, host, port):
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.address)

    def manage_connection(self):
        print("""
Commands availible:
- help
- info
- uptime
- stop """)
        while True:
            user_command = input('Enter the command!: ')
            self.socket.sendall(json.dumps({'command': user_command}).encode('utf8'))
            return_msg = self.socket.recv(1024).decode('utf-8')
            return_msg = json.loads(return_msg)
            if return_msg['message'] == 'stop':
                print('Server is shutting down!')
                break
            else:
                for key, desc in return_msg['message'].items():
                    print(f'{key} - {desc}')
                
                
if __name__ == '__main__':
    client = Client('127.0.0.1', 64321)
    client.manage_connection()