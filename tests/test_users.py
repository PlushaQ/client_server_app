import json
import unittest

from database.database import ClientServerDatabase
from users.users import User

class TestUsers(unittest.TestCase):
    def setUp(self):
        
        # create a new user and initialize fake json files
        self.user = User()
        self.user.db = ClientServerDatabase('test_database.env')
        

        self.user_to_login = {'username': 'test1', 'password': 'test'}

        self.user.register_user('test1', 'test')
        self.user.register_user('admin', 'password', 'admin')
        
        
        self.user.login_user(self.user_to_login['username'], self.user_to_login['password'])

    def tearDown(self):
        with self.user.db.db_conn as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE users, messages")
            cursor.close()


    def test_register_new_user(self):
        user = {'username': 'test_user', 'password': 'pass'}
        self.user.register_user(user['username'], user['password'])
        users = self.user.db.get_list_of_users()
        self.assertIn(user['username'], users)
    
    def test_register_user_with_existing_username(self):
        user = {'username': 'test_user', 'password': 'pass'}
        user2 = {'username': 'test_user', 'password': 'pass'}
        self.user.register_user(user['username'], user['password'])
        expected_output = json.dumps({'message': {'sign up': f'User {user2["username"]} already exists'}}, indent=1)
        
        self.assertEqual(
            self.user.register_user(user2['username'], user2['password']),
            expected_output
            )
        
    def test_login_with_correct_details(self):
        user = {'username': 'admin', 'password': 'password'}
        msg = self.user.login_user(user['username'], user['password'])
        expected_output = json.dumps({'message': {'log in': f'User {user["username"]} logged in successfully'}})
        
        self.assertEqual(msg, expected_output)
        self.assertEqual(self.user.username, user['username'])

    def test_login_with_incorrect_details(self):
        self.user.username = None
        self.user.role = None
        user = {'username': 'test2', 'password': 'test'}
        msg = self.user.login_user(user['username'], user['password'])
        expected_output = json.dumps({'message': {'log in': 'User with this username doesn\'t exist or password is incorrect'}})
        
        self.assertEqual(msg, expected_output)
        self.assertIsNone(self.user.username)

    def test_display_user_list_without_logging(self):
        self.user.username = None
        self.user.role = None
        msg = self.user.user_list()
        expected_output = json.dumps({'message': {'privileges': 'You need to login to access this!'}})
        self.assertEqual(msg, expected_output)


    def test_display_user_list_with_login(self):
        expected_output = json.dumps({'message': {1: 'test1', 2:'admin'}})
        msg = self.user.user_list()
        self.assertEqual(msg, expected_output)

    def test_send_msg_to_existing_user(self):
        self.user.send_message('admin', 'Hey', self.user.username)
        self.user.send_message('admin', 'How are you?', self.user.username)

        messages = self.user.db.get_user_messages('admin')
        self.assertIn('Hey', messages['1']['body'])
        self.assertIn('How are you?', messages['2']['body'])

    def test_send_msg_to_non_existing_user(self):
        username = 'non_existing_user'
        msg = self.user.send_message(username, 'Hey', self.user.username)
        expected_output = json.dumps({'message': {'error': f'User with username `{username}` doesn\'t exists!'}})
        
        self.assertEqual(msg, expected_output)

    def test_send_six_msg_to_check_if_inbox_is_full(self):
        self.user.send_message('admin', 'Hey', self.user.username)
        for x in range(6):
            if x == 5:
                msg = self.user.send_message('admin', 'Hey', self.user.username)
            else:
                self.user.send_message('admin', 'Hey', self.user.username)
        
        expected_output = json.dumps({'message': {'error': "Receiver has too many unread messages"}})     
        self.assertEqual(msg, expected_output)

    def test_show_full_inbox_without_any_messages(self):
        msg = self.user.show_inbox(self.user.username, 'inbox')
        expected_output = json.dumps({'message': {'Empty inbox': 'You don\'t have messages'}})
        self.assertEqual(msg, expected_output)

    def test_show_full_inbox_for_logged_user(self):
        self.user.send_message(self.user.username, 'Hey', 'admin')
        messages = self.user.db.get_user_messages(self.user.username)
        response = json.loads(self.user.show_inbox(self.user.username, 'inbox'))['message']['inbox_messages']
        self.assertEqual(messages, response)

    def test_show_full_inbox_for_other_user(self):
        self.user.send_message('admin', 'Hey', self.user.username)
        msg = json.dumps({'message': {'error': 'This isn\'t your inbox!'}})
        response = self.user.show_inbox('admin', 'inbox')
        self.assertEqual(msg, response)

    def test_show_full_inbox_for_other_user_but_with_admin_role(self):
        self.user.username = 'admin'
        self.user.role = 'admin'
        self.user.send_message(self.user.username, 'Hey', 'admin')
        messages = self.user.db.get_user_messages(self.user.username)
        response = json.loads(self.user.show_inbox(self.user.username, 'inbox'))['message']['inbox_messages']
        self.assertEqual(messages, response)

    def test_marking_messages_as_unread(self):
        self.user.send_message(self.user.username, 'Hey', 'admin')
        self.user.send_message(self.user.username, 'Hey2', 'admin')
        messages = self.user.db.get_user_messages('test1')
        self.user.show_inbox('test1', 'inbox')
        messages_after = self.user.db.get_user_messages('test1')
        self.assertNotEqual(messages, messages_after)
    

if __name__ == '__main__':
    unittest.main()