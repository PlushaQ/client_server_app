import json
import unittest
import os

from users import User

class TestUsers(unittest.TestCase):
    def setUp(self):
        # create a temporary users.json file
        self.test_users_file = 'test_users.json'
        with open(self.test_users_file, 'w') as file:
            json.dump({}, file)

        # create a temporary users_inbox.json file
        self.test_messages_file = 'test_messages.json'
        with open(self.test_messages_file, 'w') as file:
            json.dump({}, file)

        # create a new user and initialize fake json files
        self.user = User()
        
        self.user.users_file = self.test_users_file
        self.user.users_inbox_file = self.test_messages_file
        
        self.user.register_user('test1', 'test')
        self.user.register_user('admin', 'password')
        

    def tearDown(self):
        # delete the temporary files
        os.remove(self.test_users_file)
        os.remove(self.test_messages_file)


    def test_register_new_user(self):
        user = {'username': 'test_user', 'password': 'pass'}
        self.user.register_user(user['username'], user['password'])
        with open(self.test_users_file, 'r', encoding='utf-8') as file:
            users = json.load(file)
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
        
    def 



if __name__ == '__main__':
    unittest.main()