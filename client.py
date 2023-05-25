import socket
import json


class Client:
    def __init__(self, host, port):
        self.address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.address)

    def manage_connection(self):
        # Print available commands for the user
        print("""
Commands availible:
- help
- info
- uptime
- stop
- register
- login """)
        while True:
            # Prompt the user to enter a command
            user_command = input('Enter the command!: ')

            # Send the user's command to the server
            self.socket.sendall(json.dumps({'command': user_command}).encode('utf8'))

            # Receive the response from the server
            return_msg = self.socket.recv(1024).decode('utf-8')
            return_msg = json.loads(return_msg)
            if return_msg['message'] == 'stop':
                 # If the server responds with 'stop', it means it is shutting down
                print('Server is shutting down!')
                self.socket.close()
                break
            else:
                if return_msg['message'] in ["Unknown command", 'No command provided']:
                    # If the server responds with an error message, print it
                    print(return_msg['message'])
                elif 'inbox_messages' in return_msg['message']:
                    # If the response contains inbox messages, print them
                    inbox_messages = return_msg['message']['inbox_messages']
                    for message_id, message_dict in inbox_messages.items():
                        print('--------------------------')
                        print(f'Message ID: {message_id}')
                        print(f'Sender: {message_dict["sender"]}')
                        print(f'Time: {message_dict["time"]}')
                        print(f'Body: {message_dict["body"]}')
                        print(f'Read: {message_dict["read"]}')
                else:
                    # If the response contains other information, print it
                    for key, desc in return_msg['message'].items():
                        print(f'{key} - {desc}')
                    
                
if __name__ == '__main__':
    # Create a client object and connect to the server
    client = Client('127.0.0.1', 64322)
    # Start managing the connection with the server
    client.manage_connection()