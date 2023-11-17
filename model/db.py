import sqlite3

db = 'model/site.db'


def create_db():
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT,
                    password TEXT,
                    age INTEGER,
                    city TEXT
                );
            """
        )
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT,
                    chatname TEXT,
                    description TEXT,
                    created_at DATETIME
                );
            """
        )
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS chat_users (
                    login TEXT,
                    chatname TEXT
                );
            """
        )
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT,
                    chatname TEXT,
                    message TEXT,
                    created_at DATETIME
                );
            """
        )
        connection.commit()


def register_new_user(login: str, password: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE login = ?", (login,))
        user = cursor.fetchone()
        if user:
            return False
        else:
            cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password))
            connection.commit()
            return True


def check_user(login: str, password: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE login = ? AND password = ?", (login, password))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False


def load_all_user_chats(login: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    SELECT chatname FROM chat_users WHERE login = ?
                """
        cursor.execute(query, (login,))
        return [row[0] for row in cursor.fetchall()]


def create_chat(login: str, chatname: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM chats WHERE chatname=?", (chatname,))
        chat = cursor.fetchone()
        if chat:
            return False
        else:
            query = """
                      INSERT INTO chats (login, chatname, created_at)
                      VALUES (?, ?, CURRENT_TIMESTAMP)
                  """
            cursor.execute(query, (login, chatname))
            connection.commit()
            return True


def add_user_to_chat(login: str, chatname: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    INSERT INTO chat_users (login, chatname)
                    VALUES (?, ?)
                """
        cursor.execute(query, (login, chatname))
        connection.commit()


def find_chat_by_name(chatname: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM chats WHERE chatname=?", (chatname,))
        chat = cursor.fetchone()
        if chat:
            return True
        else:
            return False


def load_all_messages_by_chat_name(chatname: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    SELECT login, message FROM messages WHERE chatname = ?
                """
        cursor.execute(query, (chatname,))
        return cursor.fetchall()


def send_message(login: str, chatname: str, message: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    INSERT INTO messages (login, chatname, message, created_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """
        cursor.execute(query, (login, chatname, message))
        connection.commit()


def delete_user(login: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    DELETE FROM users
                    WHERE login = ?
                """
        cursor.execute(query, (login,))
        connection.commit()


def delete_chat(login: str, chatname: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    DELETE FROM chat_users
                    WHERE login = ? AND chatname = ?
                """
        cursor.execute(query, (login, chatname))
        connection.commit()


def delete_message(login: str, chatname: str, message: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    DELETE FROM messages
                    WHERE login = ? AND chatname = ? AND message = ?
                """
        cursor.execute(query, (login, chatname, message))
        connection.commit()
