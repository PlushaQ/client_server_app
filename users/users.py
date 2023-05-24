import json
from functools import wraps
from datetime import datetime
from database.database import ClientServerDatabase

class User:
    def __init__(self) -> None:
        self.username = None
        self.role = None
        self.db = ClientServerDatabase()
   
    """  def open_user_file(self):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as file:
                users = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # If the file does not exist or is empty, create an empty dictionary
            users = {}
        return users
    
    
    def open_message_file(self, username):
        try:
            with open(self.users_inbox_file, 'r', encoding='utf-8') as file:
                messages = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            messages = {}
            if username not in messages:
                messages[username] = {} 
        else:
            if username not in messages:
                messages[username] = {} 
        return messages
    

    def save_message_file(self, messages):
        try:
            with open(self.users_inbox_file, 'w', encoding='utf-8') as file:
                json.dump(messages, file, indent=4)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return json.dumps({'message': {'error': 'There is no inbox file'}}) 
"""

    def register_user(self, username, password, role='user'):
        # Function to register new users with corresponding username and password
        users = self.db.get_list_of_users()
        if username in users:
            # Handle the case where user exists
            message = {'message': {'sign up': f'User {username} already exists'}}

            return json.dumps(message, indent=1)
        
        self.db.register_new_user(username, password, role)

        message = {'message': {'sign up': f'User {username} registered'}}

        return json.dumps(message, indent=4)

    def login_user(self, username, password):
        # Function logging user
        user = self.db.get_user(username)

        if user and user['password'] == password:
            self.username = username
            self.role = user['role']
            return json.dumps({'message': {'log in': f'User {username} logged in successfully'}})
        else:
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
        users = self.open_user_file()
        users_names = {}
        for index, user in enumerate(users.keys()):
            users_names[index + 1] = user
        return json.dumps({'message': users_names})
    
    @login_required
    def send_message(self, username, message, sender):
        users = self.open_user_file()
        # Handle the case where user exists
        if username in users.keys():
            # Block catching problems with files
            messages = self.open_message_file(username)
            unread_messages = [messages[username][m] for m in messages[username] if messages[username][m]['read'] == 'no']
            if len(unread_messages) > 5:
                return json.dumps({'message': {'error': "Receiver has too many unread messages"}})
                
            # Creating new message 
            time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_message = {'sender': sender, 'time': time, 'body': message, 'read': 'no'}

            messages[username][f"{len(messages[username]) + 1}"] = new_message

            # Saving new message
            self.save_message_file(messages)
            return json.dumps({'message': {'Message': f'Message sent to {username} at {time}.'}})
        else:
            return json.dumps({'message': {'error': f'User with username `{username}` doesn\'t exists!'}})
        
    @login_required
    def show_inbox(self, username, command):
            if username == self.username or self.role == 'admin':
                messages = self.open_message_file(username)
                
                try:
                    if command == 'inbox':
                        messages, inbox_messages = self.check_full_inbox(messages, username)
                        if inbox_messages == {}:
                            return json.dumps({'message': {'Empty inbox': 'You don\'t have messages'}})
                    elif command == 'unread':
                        messages, inbox_messages = self.check_unread(messages, username)
                        if inbox_messages == {}:
                            return json.dumps({'message': {'Empty inbox': 'You don\'t have unread messages'}})
            
                except KeyError:
                    return json.dumps({'message': {'Empty inbox': 'You don\'t have messages'}})
                
                self.save_message_file(messages)
                
                return json.dumps({'message': {'inbox_messages': inbox_messages}}, indent=1)
            else: 
                return json.dumps({'message': {'error': 'This isn\'t your inbox!'}})

    def check_unread(self, messages, username):
        inbox_messages = {}
        for message_id, message_dict in messages[username].items():
            if message_dict['read'] == 'no':
                inbox_messages[message_id] = {
                    'sender': message_dict['sender'],
                    'time': message_dict['time'],
                    'body': message_dict['body'],
                    'read': message_dict['read']
                }
            message_dict['read'] = 'yes'
        return messages, inbox_messages
        
    def check_full_inbox(self, messages, username):
        inbox_messages = {}
        for message_id, message_dict in messages[username].items():
            inbox_messages[message_id] = {
                'sender': message_dict['sender'],
                'time': message_dict['time'],
                'body': message_dict['body'],
                'read': message_dict['read']
            }
            message_dict['read'] = 'yes'
        return messages, inbox_messages
    

