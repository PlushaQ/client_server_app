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
    
    def get_user(self, username):
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


db = ClientServerDatabase()
print(db.get_user('pluhaq'))