from .database_connection import DatabaseConnection


class ClientServerDatabase:
    def __init__(self):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            username VARCHAR(255) PRIMARY KEY,
                            password VARCHAR(255),
                            role VARCHAR(5)
                            );''')
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

    def get_list_of_users(self):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username FROM users;')

            users = cursor.fetchall()
            users = [row[0] for row in users]

            cursor.close()
            return users
    
    def get_user_info(self, username):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
            try:
                user = {'username': user[0],
                        'password': user[1],
                        'role': user[2]}
            except TypeError:
                cursor.close()
                return False
            
            cursor.close()    
            return user
        
    def register_new_user(self, username, password, role):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users VALUES (%s, %s, %s)', (username, password, role))
            cursor.close()

    def get_user_messages(self, username):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT message_id, sender, time, body, is_read FROM messages WHERE username = %s', (username,))
            messages = cursor.fetchall()
            messages = {
                message[0]: {
                 'sender': message[1],
                 'time': message[2].strftime('%Y-%m-%d %H:%M:%S'),
                 'body': message[3],
                 'read': message[4]}
                  for message in messages}
            cursor.close()
            return messages
    
    def send_message(self, receiver, new_message):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages VALUES (%s, %s, %s, %s, %s, %s)',
                            (receiver,
                             new_message['message_id'],
                             new_message['sender'],
                             new_message['time'],
                             new_message['body'],
                             new_message['read']))
            cursor.close()
    
    def get_user_unread_messages(self, username):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT message_id, sender, time, body, is_read FROM messages WHERE username = %s AND is_read = 'f'" , (username,))
            messages = cursor.fetchall()
            messages = {
                message[0]: {
                 'sender': message[1],
                 'time': message[2].strftime('%Y-%m-%d %H:%M:%S'),
                 'body': message[3],
                 'read': message[4]}
                  for message in messages}
            cursor.close()
            return messages
        
    def mark_unread_as_read(self, username):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE messages SET is_read = True WHERE username = %s", (username, ))
            cursor.close()

