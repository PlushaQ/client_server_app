import json
from functools import wraps
from datetime import datetime
from database.database import ClientServerDatabase


class User:
    def __init__(self) -> None:
        self.username = None
        self.role = None
        self.db = ClientServerDatabase('database.env')
   
    def register_user(self, username, password, role='user'):
        # Function to register new users with corresponding username and password
        users = self.db.get_list_of_users()
        if username in users:
            # Handle the case where user exists
            message = {'message': {'sign up': f'User {username} already exists'}}

            return message
        
        self.db.register_new_user(username, password, role)

        message = {'message': {'sign up': f'User {username} registered'}}

        return message

    def login_user(self, username, password):
        # Function logging user
        user = self.db.get_user_info(username)

        if user and user['password'] == password:
            self.username = username
            self.role = user['role']
            return {'message': {'log in': f'User {username} logged in successfully'}}
        else:
            return {'message': {'log in': 'User with this username doesn\'t exist or password is incorrect'}}
    
    def login_required(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.username is None:
                return {'message': {'privileges': 'You need to login to access this!'}}
            return func(self, *args, **kwargs)
        return wrapper
    
    @login_required
    def user_list(self):
        # Function to retrieve the list of users
        users = self.db.get_list_of_users()
        users_names = {}
        for index, user in enumerate(users):
            users_names[index + 1] = user
        return {'message': users_names}
    
    @login_required
    def send_message(self, username, message, sender):
        # Function to send a message to another user
        users = self.db.get_list_of_users()
        # Handle the case where user exists
        if username in users:
            # Block catching problems with files
            messages = self.db.get_user_messages(username)
            unread_messages = sum(1 for message in messages if messages[message]['read'] is False)
            if unread_messages > 5:
                return {'message': {'error': "Receiver has too many unread messages"}}
                
            # Creating new message 
            time = datetime.now()
            new_message = {'message_id': len(messages) + 1, 'sender': sender, 'time': time, 'body': message, 'read': 'no'}


            # Saving new message
            self.db.send_message(username, new_message)
            return {'message': {'Message': f'Message sent to {username} at {time.strftime("%Y-%m-%d %H:%M:%S")}.'}}
        else:
            return {'message': {'error': f'User with username `{username}` doesn\'t exists!'}}
        
    @login_required
    def show_inbox(self, username, command):
        # Function to display the inbox or unread messages of a user
        if username == self.username or self.role == 'admin':
            try:
                if command == 'inbox':
                    messages = self.db.get_user_messages(username)
                    if messages == {}:
                        return {'message': {'Empty inbox': 'You don\'t have messages'}}
                elif command == 'unread':
                    messages = self.db.get_user_unread_messages(username)
                    if messages == {}:
                        return {'message': {'Empty inbox': 'You don\'t have unread messages'}}
        
            except KeyError:
                return {'message': {'Empty inbox': 'You don\'t have messages'}}

            self.db.mark_unread_as_read(username)    
            return {'message': {'inbox_messages': messages}}
        else: 
            return {'message': {'error': 'This isn\'t your inbox!'}}

    

