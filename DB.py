import sqlite3


class DB:
    def __init__(self):
        conn = sqlite3.connect('messages.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (user_name VARCHAR(50) PRIMARY KEY,
                             name VARCHAR(50),
                             surname VARCHAR(50),
                             password_hash VARCHAR(128),
                             age INTEGER,
                             email VARCHAR(100)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, name, surname, email, age):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, name, surname, email, age) 
                          VALUES (?,?,?,?,?,?)''', (user_name, password_hash, name, surname, email, age))
        cursor.close()
        self.connection.commit()

    def get(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", (user_name,))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True,) if row else (False,)

    def exist(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?",
                       (user_name,))
        row = cursor.fetchone()
        return (True,) if row else (False,)


class InboxMessageModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS inbox_messages 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             user_name VARCHAR(50),
                             recipient VARCHAR(50)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, user_name, recipient):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO inbox_messages 
                          (title, content, user_name, recipient) 
                          VALUES (?,?,?,?)''', (title, content, user_name, recipient))
        cursor.close()
        self.connection.commit()

    def get(self, message_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM inbox_messages WHERE id = ?", (str(message_id)))
        row = cursor.fetchone()
        return row

    def get_all(self, user_name=None, recipient=None):
        cursor = self.connection.cursor()
        if user_name:
            cursor.execute("SELECT * FROM inbox_messages WHERE user_name = ?",
                           (user_name, ))
        elif recipient:
            cursor.execute("SELECT * FROM inbox_messages WHERE recipient = ?",
                           (recipient, ))
        else:
            cursor.execute("SELECT * FROM inbox_messages")
        rows = cursor.fetchall()
        return rows

    def delete(self, message_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM inbox_messages WHERE id = ?''', (str(message_id)))
        cursor.close()
        self.connection.commit()

    def exist(self, message_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?",
                       (message_id,))
        row = cursor.fetchone()
        return (True,) if row else (False,)


class OutboxMessageModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS outbox_messages 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             user_name VARCHAR(50),
                             recipient VARCHAR(50)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, user_name, recipient):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO outbox_messages 
                          (title, content, user_name, recipient) 
                          VALUES (?,?,?,?)''', (title, content, user_name, recipient))
        cursor.close()
        self.connection.commit()

    def get(self, message_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM outbox_messages WHERE id = ?", (str(message_id)))
        row = cursor.fetchone()
        return row

    def get_all(self, user_name=None, recipient=None):
        cursor = self.connection.cursor()
        if user_name:
            cursor.execute("SELECT * FROM outbox_messages WHERE user_name = ?",
                           (user_name, ))
        elif recipient:
            cursor.execute("SELECT * FROM outbox_messages WHERE recipient = ?",
                           (recipient, ))
        else:
            cursor.execute("SELECT * FROM outbox_messages")
        rows = cursor.fetchall()
        return rows

    def delete(self, message_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM outbox_messages WHERE id = ?''', (str(message_id)))
        cursor.close()
        self.connection.commit()
