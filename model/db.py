import sqlite3

db = 'model/site.db'


def create_db():
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE,
                                password TEXT
                            )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS list_chats (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                chat_name TEXT,
                                created_by TEXT,
                                FOREIGN KEY (created_by) REFERENCES users (username)
                            )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS chat (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                chat_id INTEGER,
                                username TEXT,
                                time INTEGER,
                                message TEXT,
                                FOREIGN KEY (chat_id) REFERENCES list_chats (id)
                            )''')

        connection.commit()


def create_new_chat(chat_name: str, created_by: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM list_chats WHERE chat_name=?", (chat_name,))
        chat = cursor.fetchone()
        if chat:
            return False
        else:
            cursor.execute("INSERT INTO list_chats (chat_name, created_by) VALUES (?, ?)", (chat_name, created_by))
            connection.commit()
            return True


def add_new_message_to_chat(chat_name: str, username: str, time, message: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO chat (chat_id, username, time, message)
                            VALUES ((SELECT id FROM list_chats WHERE chat_name=?), ?, ?, ?)
                            ''', (chat_name, username, time, message))
        connection.commit()


def find_chat_by_name(chat_name: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM list_chats WHERE chat_name=?", (chat_name,))
        chat = cursor.fetchone()
        if chat:
            return True
        else:
            return False


def load_all_user_chats(username: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT chat_name FROM list_chats WHERE created_by=?", (username,))
        user_list_chats = [row[0] for row in cursor.fetchall()]
        return user_list_chats


def load_all_messages_by_chat_name(chat_name: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = '''
                SELECT chat.message, users.username
                FROM chat
                INNER JOIN list_chats ON chat.chat_id = list_chats.id
                INNER JOIN users ON chat.username = users.username
                WHERE list_chats.chat_name=?
                ORDER BY chat.time ASC;
                '''
        cursor.execute(query, (chat_name,))
        results = cursor.fetchall()
        return results


def register_new_user(username: str, password: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user:
            return False
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            connection.commit()
            return True


def check_user(username: str, password: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False
