import unittest
import socket
import json
import threading
from random import choice

from server import Server


class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        self.host = '127.0.0.1'
        self.ports = range(64322, 64390)
        self.port = choice(self.ports)

        # Initialize the Server instance and event to signal when server is ready
        self.server = Server(self.host, self.port, 'test_database.env')
        self.server_ready_event = threading.Event()

        # Create a client socket and event to signal when client is ready
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_ready_event = threading.Event()

        self.server_thread = None
        self.client_thread = None

        self.start_server()
        self.start_client()

        self.client_ready_event.wait()

    def tearDown(self):
        # Close the server socket and the client socket
        self.client.close()
        self.server.stop()

    def start_server(self):
        def run_server():
            self.server.run()

        self.server_thread = threading.Thread(target=run_server)
        self.server_thread.start()
        self.server_ready_event.set()

    def start_client(self):
        def run_client():
            self.server_ready_event.wait()
            self.client.connect((self.host, self.port))
            self.client_ready_event.set()

        self.client_thread = threading.Thread(target=run_client)
        self.client_thread.start()

    def test_available_commands_before_login(self):
        # Test the available_commands_before_login method
        expected_return = {'message': {
            'uptime': "returns the uptime of the server",
            'info': "returns version of server and it's date creation",
            'help': "show list of commands",
            'stop': "stops server and client",
            'register': 'registers new users. usage: <register username password>',
            'login': 'log in user. usage: <login username password>'
        }}
        self.client.send(json.dumps({'command': 'help'}).encode('utf-8'))
        data = self.client.recv(1024).decode('utf-8')
        self.assertEqual(json.loads(data), expected_return)

    def test_available_commands_after_login(self):
        # Test the available_commands_after_login method
        self.server.handler.user.username = 'test_user'
        expected_return = {'message': {
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
        }}
        self.client.send(json.dumps({'command': 'help'}).encode('utf-8'))
        data = self.client.recv(1024).decode('utf-8')
        self.assertEqual(json.loads(data), expected_return)

    def test_uptime(self):
        # Test the uptime property
        self.client.send(json.dumps({'command': 'uptime'}).encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode('utf-8'))
        data = data['message']
        self.assertRegex(data['uptime'], r'^[0-9]+:[0-9]+:[0-9]+\.[0-9]{6}$')

    def test_info(self):
        # Test the info property
        self.client.send(json.dumps({'command': 'info'}).encode('utf-8'))
        data = json.loads(self.client.recv(1024).decode('utf-8'))
        data = data['message']
        self.assertRegex(data['Version'], r'^[0-9]+.[0-9]+.[0-9]+$')
        self.assertEqual(data['Creation_date'], str(self.server.server_start_time))


if __name__ == '__main__':
    unittest.main()
