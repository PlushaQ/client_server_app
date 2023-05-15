import unittest
import socket


from server import Server
from users.users import User



class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        self.host = '127.0.0.1'
        self.port = 64322
        
        self.server = Server(self.host, self.port)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.user = User()
    
    def tearDown(self):
        self.server.socket.close()
        self.client.close()

    def test_available_commands_before_login(self):
        expected_return = {'message': {
            'uptime': "returns the uptime of the server",
            'info': "returns version of server and it's date creation",
            'help': "show list of commands",
            'stop': "stops server and client",
            'register': 'registers new users. usage: <register username password>',
            'login': 'log in user. usage: <login username password>'
        }}
        self.assertEqual(self.server.available_commands_before_login(), expected_return)

    def test_available_commands_after_login(self):
        self.server.user.username = 'test_user'
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
        self.assertEqual(self.server.available_commands_after_login(), expected_return)
        
    def test_uptime(self):
        uptime_str = self.server.uptime['message']['uptime']
        self.assertRegex(uptime_str, r'^[0-9]+:[0-9]+:[0-9]+\.[0-9]{6}$')

    def test_info(self):
        info_dict = self.server.info['message']
        self.assertRegex(info_dict['Version'], r'^[0-9]+.[0-9]+.[0-9]+$')
        self.assertEqual(info_dict['Creation_date'], str(self.server.server_start_time))


if __name__ == '__main__':
    unittest.main()
