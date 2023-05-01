import json
from functools import wraps
from datetime import datetime

class User:
    def __init__(self) -> None:
        self.username = None
        self.role = None
    
    @staticmethod
    def open_user_file():
        try:
            with open('users.json', 'r', encoding='utf-8') as file:
                users = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # If the file does not exist or is empty, create an empty dictionary
            users = {}
        return users

    @staticmethod
    def register_user(username, password):
        # Function to register new users with corresponding username and password
        users = User.open_user_file()
        if username in users.keys():
            # Handle the case where user exists
            message = {'message': {'sign up': f'User {username} already exists'}}
            print(message)
            return json.dumps(message, indent=1)
        
        users[username] = {'password': password, 'role': 'user'}

        with open('users.json', 'w', encoding='utf-8') as file:
            json.dump(users, file, indent=4)
        message = {'message': {'sign up': f'User {username} registered'}}
        print(message) 
        return json.dumps(message, indent=4)

    def login_user(self, username, password):
        # Function logging user
        users = User.open_user_file()
        
        if username in users.keys() and password == users[username]['password']:
            self.username = username
            self.role = users[username]['role']
            print({'message': {'log in': f'User {username} logged in successfully'}})
            return json.dumps({'message': {'log in': f'User {username} logged in successfully'}})
        else:
            print({'message': 'User with this username doesn\'t exist or password is incorrect'})
            return json.dumps({'message': {'log in': 'User with this username doesn\'t exist or password is incorrect'}})
    
    def login_required(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.username is None:
                return json.dumps({'message': {'privileges': 'You need to login to access this!'}})
            return func(self, *args, **kwargs)
        return wrapper
    
    @login_required
    def user_list(self):
        users = User.open_user_file()
        users_names = {}
        for index, user in enumerate(users.keys()):
            users_names[index + 1] = user
        return json.dumps({'message': users_names})
    
    @login_required
    def send_message(self, username, message, sender):
        users = User.open_user_file()
        # Handle the case where user exists
        if username in users.keys():
            # Block catching problems with files
            try:
                with open('users_inbox.json', 'r', encoding='utf-8') as file:
                    messages = json.load(file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                messages = {}
                if username not in messages:
                    messages[username] = {} 
            else:
                if username not in messages:
                    messages[username] = {} 
                unread_messages = [messages[username][m] for m in messages[username] if messages[username][m]['read'] == 'no']
                print(f'unread = {len(unread_messages)}')
                if len(unread_messages) > 5:
                    return json.dumps({'message': {'error': "Receiver has too many unread messages"}})
                
            # Creating new message 
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_message = {'sender': sender, 'time': time, 'body': message, 'read': 'no'}

            messages[username][f"{len(messages[username]) + 1}"] = new_message

            # Saving new message
            try:
                with open('users_inbox.json', 'w', encoding='utf-8') as file:
                    json.dump(messages, file, indent=4)
                    return json.dumps({'message': {'Message': f'Message sent to {username} at {time}.'}})
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                return json.dumps({'message': {'error': 'There is no inbox file'}})
        else:
            return json.dumps({'message': {'error': f'User with username `{username}` doesn\'t exists!'}})
        
    @login_required
    def show_inbox(self, username):
            if username == self.username:
                try:
                    with open('users_inbox.json', 'r', encoding='utf-8') as file:
                        messages = json.load(file)
                except (FileNotFoundError, json.decoder.JSONDecodeError):
                    return json.dumps({'message': {'error': 'There is no inbox file'}})
                
                inbox_messages = {}
                for message_id, message_dict in messages[username].items():
                    message_dict['read'] = 'yes'
                    inbox_messages[message_id] = {
                        'sender': message_dict['sender'],
                        'time': message_dict['time'],
                        'body': message_dict['body']
                    }
                
                try:
                    with open('users_inbox.json', 'w', encoding='utf-8') as file:
                        json.dump(messages, file, indent=4)
                except (FileNotFoundError, json.decoder.JSONDecodeError):
                    return json.dumps({'message': {'error': 'There is no inbox file'}})
                
                print(inbox_messages)
                return json.dumps({'message': {'inbox_messages': inbox_messages}}, indent=1)

    @login_required
    def check_unread(self, username):
        if username == self.username or self.role == 'admin':
            try:
                with open('users_inbox.json', 'r', encoding='utf-8') as file:
                    messages = json.load(file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                return json.dumps({'message': {'error': 'There is no inbox file'}})
            
            inbox_messages = {}
            for message_id, message_dict in messages[username].items():
                if message_dict['read'] = 'no':
                    inbox_messages[message_id] = {
                        'sender': message_dict['sender'],
                        'time': message_dict['time'],
                        'body': message_dict['body']
                    }
                message_dict['read'] = 'yes'
            
            try:
                with open('users_inbox.json', 'w', encoding='utf-8') as file:
                    json.dump(messages, file, indent=4)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                return json.dumps({'message': {'error': 'There is no inbox file'}})
            
            print(inbox_messages)
            return json.dumps({'message': {'inbox_messages': inbox_messages}}, indent=1)

    

