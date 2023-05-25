# simple_client_server_app
This is a client-server application where the client can send a command to the server, and the server returns the appropriate response based on the command.
## Installation

    This application requires Python 3 to run and postgresql installed in your computer. Clone the repository and navigate to the directory in the command line.

### Starting the server

    To start the server, run the following command in the command line:

    python server.py

    By default, the server will listen on 127.0.0.1:64321.

### Starting the client

    To start the client, run the following command in a separate command line window:

    python client.py

    The client will connect to the server and display a list of available commands. Enter a command to receive a response from the server.

The available commands before login are:

    'uptime': 'returns the uptime of the server',
    'info': 'returns version of server and it's date creation',
    'help': 'show list of commands',
    'stop': 'stops server and client',
    'register': 'registers new users. usage: <register username password>',
    'login': 'log in user. usage: <login username password>',

The available commands after login are expanded to:

    'send': 'send user a message. usage <send user message(max. 255 chars)>',
    'unread': 'shows unread messages from users inbox. usage <unread username>',
    'inbox': 'shows users inbox. usage: <inbox username>',
    'user_list': 'shows users in the server'  
  
