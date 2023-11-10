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
                                name TEXT,
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


def create_new_chat(name: str, created_by: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM list_chats WHERE name=?", (name,))
        chat = cursor.fetchone()
        if chat:
            return False
        else:
            cursor.execute("INSERT INTO list_chats (name, created_by) VALUES (?, ?)", (name, created_by))
            connection.commit()
            return True


def add_new_message_to_chat(name, username, time, message):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO chat (chat_id, username, time, message)
                            VALUES ((SELECT id FROM list_chats WHERE name=?), ?, ?, ?)
                            ''', (name, username, time, message))
        connection.commit()


def find_chat_by_name(name: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM list_chats WHERE name=?", (name,))
        chat = cursor.fetchone()
        if chat:
            return True
        else:
            return False


def load_all_user_chats(username: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM list_chats WHERE created_by=?", (username,))
        user_list_chats = [row[0] for row in cursor.fetchall()]
        return user_list_chats


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


def select_chat():
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute('''
                            SELECT
                                chat.id,
                                chat.name,
                                chat.created_by,
                                chat.username,
                                chat.time,
                                chat.message
                            FROM
                                chat
                            INNER JOIN
                                chats
                            ON
                                chat.chat_id = chats.id
                            WHERE
                                chats.name = 'Chat 1';
                        ''')
        results = cursor.fetchall()
        for row in results:
            print(row)
