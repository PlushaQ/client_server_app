# simple_client_server_app
This is a client-server application where the client can send a command to the server, and the server returns the appropriate response based on the command.

## Description
    This application allows clients to interact with a server by sending commands and receiving corresponding responses. The server handles these commands and provides the requested information or performs the requested actions.

    Please note that the current version of the application only supports a single client connection. However, a multi-user version is currently under development and will be available soon.    

## Installation

    To run this application, you need to have Python 3 installed on your computer, as well as PostgreSQL for the upcoming multi-user version. Follow the steps below to install and set up the application:

    Clone the repository to your local machine.

    Navigate to the repository directory using the command line.
    

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

### Database Setup (Multi-User Version - Coming Soon)

The upcoming multi-user version of the application will require PostgreSQL for database functionality. Detailed instructions for setting up the database will be provided in the updated README once the multi-user version is released.

### License
This project is licensed under the MIT License.

The MIT License is a permissive open-source license that allows you to freely use, modify, and distribute the code in this repository. It comes with minimal restrictions and provides maximum flexibility for developers and users of the software.