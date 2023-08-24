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

### Database Setup (Multi-User Version)

The multi-user version of the application requires PostgreSQL for database functionality. 

#### To set up database:

Create a new database:

Open a terminal or command prompt and log in to PostgreSQL using the psql command:

    psql -U postgres

Once logged in, you can create a new database using the following command:

    CREATE DATABASE your_database_name;

Replace your_database_name with the desired name for your database.

#### Create a new user:
While still in the psql prompt, create a new user and set a password for it using the following command:

    CREATE USER your_username WITH PASSWORD 'your_password';

Replace your_username and your_password with the desired username and password for the new user.

#### Grant privileges to the user:
To allow the new user to access the database and perform operations on it, grant the necessary privileges using the following command:

    GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;

Replace your_database_name and your_username with the appropriate names.

#### Update database.env:
In the main directory of your application, create a file named database.env if it doesn't already exist. Update its content with the database connection details:

    user=your_username
    password=your_password
    host=127.0.0.1
    port=5432
    database=your_database_name

Replace the placeholders with the actual values you set for your PostgreSQL user and database.

With the database set up and the database.env file configured, you can now run the multi-user version of the application. When the server starts, it will connect to the PostgreSQL database using the provided credentials.
### License
This project is licensed under the MIT License.

The MIT License is a permissive open-source license that allows you to freely use, modify, and distribute the code in this repository. It comes with minimal restrictions and provides maximum flexibility for developers and users of the software.