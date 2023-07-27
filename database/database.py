from .database_pool_connection import DatabaseConnectionPoolManager
import time


class ClientServerDatabase:
    db = None

    def __init__(self, database, time_limit='x'):
        # Initialize the ClientServerDatabase object

        self.db_conn_pool = DatabaseConnectionPoolManager(
            database, time_limit)  # Create a DatabaseConnection object with the specified database

        # Create DB if it's empty
        conn = self.db_conn_pool.start_new_connection()
        cursor = conn.cursor()

        # Create the 'users' table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username VARCHAR(255) PRIMARY KEY,
                        password VARCHAR(255),
                        role VARCHAR(5)
                        );''')

        # Create the 'messages' table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        username VARCHAR(255) REFERENCES users (username),
                        message_id INTEGER,
                        sender VARCHAR(255),
                        time TIMESTAMP,
                        body TEXT,
                        is_read BOOLEAN,
                        PRIMARY KEY (username, message_id)
        );''')
        cursor.close()
        conn.commit()
        self.db_conn_pool.return_connection_to_pool(conn)

        ClientServerDatabase.db = self

    def close_connections(self):
        self.db_conn_pool.close_all_connections()

    def db_query(self, sql_query):
        try:
            conn = self.db_conn_pool.start_new_connection()
            if conn is None:
                time.sleep(2)
                return self.db_query(sql_query)
            else:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                data = cursor.fetchall()
                cursor.close()
                self.db_conn_pool.return_connection_to_pool(conn)
                return data

        except Exception as e:
            print(e)

    def get_list_of_users(self):
        # Retrieve a list of usernames from the 'users' table
        query = 'SELECT username FROM users;'
        users = self.db_query(query)
        users = [row[0] for row in users]
        return users

    def get_user_info(self, username):
        # Retrieve information about a user from the 'users' table
        query = 'SELECT * FROM users WHERE username = %s', (username,)
        user = self.db_query(query)[0]
        try:
            user = {'username': user[0],
                    'password': user[1],
                    'role': user[2]}
        except TypeError:
            return False

        return user

    def register_new_user(self, username, password, role):
        # Register a new user in the 'users' table
        query = 'INSERT INTO users VALUES (%s, %s, %s)', (username, password, role)
        self.db_query(query)

    def get_user_messages(self, username):
        # Retrieve messages for a specific user from the 'messages' table
        query = 'SELECT message_id, sender, time, body, is_read FROM messages WHERE username = %s', (username,)
        messages = self.db_query(query)
        messages = {
            str(message[0]): {
                'sender': message[1],
                'time': message[2].strftime('%Y-%m-%d %H:%M:%S'),
                'body': message[3],
                'read': message[4]}
            for message in messages}
        return messages

    def send_message(self, receiver, new_message):
        # Insert a new message into the 'messages' table
        query = ('INSERT INTO messages VALUES (%s, %s, %s, %s, %s, %s)',
                 (receiver,
                  new_message['message_id'],
                  new_message['sender'],
                  new_message['time'],
                  new_message['body'],
                  new_message['read']))
        self.db_query(query)

    def get_user_unread_messages(self, username):
        # Retrieve unread messages for a specific user from the 'messages' table
        query = ("SELECT message_id, sender, time, body, is_read FROM messages WHERE username = %s AND is_read = 'f'",
                 (username,))
        messages = self.db_query(query)
        messages = {
            str(message[0]): {
                'sender': message[1],
                'time': message[2].strftime('%Y-%m-%d %H:%M:%S'),
                'body': message[3],
                'read': message[4]}
            for message in messages
        }

        return messages

    def mark_unread_as_read(self, username):
        # Mark unread messages as read for a specific user in the 'messages' table
        query = "UPDATE messages SET is_read = True WHERE username = %s", (username,)
        self.db_query(query)
