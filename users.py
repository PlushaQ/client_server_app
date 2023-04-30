import json
from functools import wraps
from datetime import datetime

class User:
    def __init__(self) -> None:
        self.login = None
        self.role = None

    @staticmethod
    def register_user(login, password):
        # Function to register new users with corresponding login and password
        try:
            with open('users.json', 'r', encoding='utf-8') as file:
                users = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # If the file does not exist or is empty, create an empty dictionary
            users = {}
        if login in users.keys():
            # Handle the case where user exists
            message = {'message': f'User {login} already exists'}
            return json.dumps(message, indent=1)
        
        users[login] = {'password': password, 'role': 'user'}

        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump(users, file)
        message = f'User {login} registered'

        return json.dumps(message, indent=1)

    def login_user(self, login, password):
        # Function logging user
        try:
            with open('users.json', 'r', encoding='utf-8') as file:
                users = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # If the file does not exist or is empty, create an empty dictionary
            return json.dumps({'message': "Missing or corrupted user database"})
        
        if login in users.keys() and password == users[login][password]:
            self.login = login
            self.role = users[login]['role']
            print({'message': f'User {login} logged in successfully'})
            return json.dumps({'message': f'User {login} logged in successfully'})
        else:
            print({'message': 'User with this login doesn\'t exist or password is incorrect'})
            return json.dumps({'message': 'User with this login doesn\'t exist or password is incorrect'})
            
    @staticmethod
    def admin_required(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.role != 'admin':
                print('bbb')
                return json.dumps({'message': "You don't have access to this"})
            return func(self, *args, **kwargs)
        return wrapper
 
    def user_list(self):
        try:
            with open('users.json', 'r', encoding='utf-8') as file:
                users = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return json.dumps({'message': "Missing or corrupted user database"})

        for index, user in enumerate(users.keys()):
            print(f'{index + 1}. {user}')
    
    def show_inbox(self) -> json:
        pass

    def check_unread():
        pass

    @admin_required
    def check_other_user_messages(self):
        print('ppp')


User.register_user('test123', 'test125')
user = User()
user.check_other_user_messages()
user.login_user('plushaq', 'password')
user.check_other_user_messages()
user.user_list()