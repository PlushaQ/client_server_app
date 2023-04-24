# simple_client_server_app
This is a client-server application where the client can send a command to the server, and the server returns the appropriate response based on the command.
Installation

This application requires Python 3 to run. Clone the repository and navigate to the directory in the command line.
## Usage

### Starting the server

    To start the server, run the following command in the command line:

    python server.py

    By default, the server will listen on 127.0.0.1:64321.

### Starting the client

    To start the client, run the following command in a separate command line window:

    python client.py

    The client will connect to the server and display a list of available commands. Enter a command to receive a response from the server.

The available commands are:

    help: show the list of commands
    info: return the version of the server and its date of creation
    uptime: return the uptime of the server
    stop: stop the server and the client
