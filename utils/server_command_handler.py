from datetime import datetime
from users.users import User

class ServerResponseHandler:
    """
    Class to manage function call to make server code easier to read
    """
    def __init__(self, date_of_creation) -> None:
        self.server_start_time = date_of_creation
        self.user = User()


    def available_commands_before_login(self):
        # Returns a dictionary of available commands before user login.
        commands = {
            'uptime': "returns the uptime of the server",
            'info': "returns version of server and it's date creation",
            'help': "show list of commands",
            'stop': "stops server and client",
            'register': 'registers new users. usage: <register username password>',
            'login': 'log in user. usage: <login username password>'

        }
        return {'message': commands}

    def available_commands_after_login(self):
        # Returns a dictionary of available commands after user login.
        commands = {
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
        }
        return {'message': commands}

    def uptime(self, command):
        # Returns an uptime of the server
        uptime = {"uptime": str(datetime.now() - self.server_start_time)}
        print(f'Sending uptime to client')
        return {'message': uptime}

    def info(self, command):
        # Returns a server info
        info = {
            'Version': '2.0.0',
            'Creation_date': str(self.server_start_time),
        }
        print(f'Sending uptime to client')
        return {'message': info}
        
    def help(self, command):
        # Returns a list of commands
        print(f'Sending command list to client ')
        if self.user.username is None:
            return self.available_commands_before_login()
        else:
            return self.available_commands_after_login()
    
    def register(self, command):
        # Returns info about register and call registering function 
        if len(command) != 3:
            print('Sending usage information to client')
            return {'message': {'Usage': '<register username password>'}}
            
        else:
            print('User registered')
            return self.user.register_user(command[1], command[2])
    
    def login(self, command):
        # Returns info about login and call login function 
        if len(command) != 3:
            print('Sending usage information to client')
            return {'message': {'Usage': '<login username password>'}}
        else:
            print(f"Logged {self.user.username} with role {self.user.role}")
            return self.user.login_user(command[1], command[2])
            
    def user_list(self, command):
        # Returns user list 
        print('Sending to client user list')
        return self.user.user_list()
    
    def send(self, command):
        # Returns info about sending and call send message function
        if len(command) < 3:
            print('Sending usage information to client')
            return {'message': {'Usage': '<send username message>'}}
        else:
            print(f'Sending messages from {self.user.username} to {command[1]}')
            return self.user.send_message(command[1], ' '.join(command[2:]), self.user.username)

    def inbox_or_unread(self, command):
        # Returns inbox or unread inbox 
        if len(command) != 2:
            command.append(self.user.username)
            print(f'Showing {command[1]} inbox.')
            return self.user.show_inbox(command[1], command[0])

    def handle_commands(self, command):
        # Main function to call other functions 
        functions = {
            'uptime': self.uptime,
            'info': self.info,
            'help': self.help,
            'register': self.register,
            'login': self.login,
            'user_list': self.user_list,
            'send': self.send,
            'inbox': self.inbox_or_unread, 
        }
        
        if not command:
            print(f'Client send command - "" ')
            print('Sending "No command provided" to client')
            return {'message': 'No command provided'}
        
        elif command[0] not in functions.keys():
            print(f'Client send command - {command[0]}')
            print('Sending "Unknown command" to client')
            return {'message': 'Unknown command'}

        else:
            print(f'Client send command - {command[0]}')
            selected_function = functions[command[0]]
            return selected_function(command)
