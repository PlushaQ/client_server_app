import json
from functools import wraps
from datetime import datetime

class User:
    def __init__(self) -> None:
        self.username = None
        self.role = None

    @staticmethod
    def register_user(username, password):
        # Function to register new users with corresponding username and password
        try:
            with open('users.json', 'r', encoding='utf-8') as file:
                users = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # If the file does not exist or is empty, create an empty dictionary
            users = {}
        if username in users.keys():
            # Handle the case where user exists
            message = {'message': {'sign up': f'User {username} already exists'}}
            print(message)
            return json.dumps(message, indent=1).encode('utf-8')
        
        users[username] = {'password': password, 'role': 'user'}

        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump(users, file)
        message = {'message': {'sign up': f'User {username} registered'}}
        print(message) 
        return json.dumps(message, indent=1)

    def login_user(self, username, password):
        # Function logging user
        try:
            with open('users.json', 'r', encoding='utf-8') as file:
                users = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # If the file does not exist or is empty, create an empty dictionary
            return json.dumps({'message': {'log in': "Missing or corrupted user database"}})
        
        if username in users.keys():
            if password == users[username]['password']:
                self.username = username
                self.role = users[username]['role']
                print({'message': {'log in': f'User {username} logged in successfully'}})
                return json.dumps({'message': {'log in': f'User {username} logged in successfully'}})
        else:
            print({'message': 'User with this username doesn\'t exist or password is incorrect'})
            return json.dumps({'message': {'log in': 'User with this username doesn\'t exist or password is incorrect'}})
            
    @staticmethod
    def admin_required(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.role != 'admin':
                return json.dumps({'message': {'privileges': "You don't have access to this"}})
            return func(self, *args, **kwargs)
        return wrapper
 
    def user_list(self):
        try:
            with open('users.json', 'r', encoding='utf-8') as file:
                users = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return json.dumps({'message': {'error': "Missing or corrupted user database"}})
        users_names = {}
        for index, user in enumerate(users.keys()):
            users_names[index + 1] = user
        return json.dumps({'message': users_names})
    
    def send_message(self, username, message, sender):
        try:
            with open('users_inbox.json', 'r', encoding='utf-8') as file:
                messages = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return json.dumps({'message': {'error': 'There is no inbox file'}})
        
        unread_messages = [m for m in messages[username] if m.get('read', '') == 'no']

        if len(unread_messages) > 5:
            return json.dumps({'message': {'error': "Receiver has too many unread messages"}})
        else:
            messages[username] += {'sender': sender, 'time': datetime.now(), 'body': message, 'read': 'no'}
        
        try:
            with open('users_inbox.json', 'w', encode='utf-8') as file:
                json.dump(messages, file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return json.dumps({'message': {'error': 'There is no inbox file'}})
    
        
    
    def show_inbox(self, username):
        try:
            with open('users_inbox.json', 'r', encoding='utf-8') as file:
                messages = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return json.dumps({'message': {'error': 'There is no inbox file'}})
        
        for index, message in enumerate(messages[username]):
            message['read'] = 'yes'
            print(f'{index + 1}. From {message["sender"]} at {message["time"]}. \n {message["body"]}')

    def check_unread(self, username):
        pass
    
    @admin_required
    def check_other_unread(self, username):
        pass

    @admin_required
    def check_other_user_messages(self, username):
        print('ppp')

