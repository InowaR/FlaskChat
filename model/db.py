import sqlite3

db = 'model/site.db'


def create_db():
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """
        )
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chatname TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        )
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
        )
        """
        )
        connection.commit()


def register_new_user(username: str, password: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user:
            print("Пользователь существует")
            return False
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            connection.commit()
            return True


def check_user(username: str, password: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            print("Логин и пароль совпадают")
            return True
        else:
            return False


def load_all_user_chats(username: str):
    with (sqlite3.connect(db) as connection):
        cursor = connection.cursor()
        query = """ SELECT u.id, c.chatname
                    FROM users u
                    JOIN chats c ON u.id = c.user_id
                    WHERE u.username=?
                """
        cursor.execute(query, (username,))
        return [row[1] for row in cursor.fetchall()]


def create_new_chat(username: str, chatname: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM chats WHERE chatname = ?", (chatname,))
        chat = cursor.fetchone()
        if chat:
            print("Чат существует")
            return False
        else:
            query = """ INSERT INTO chats (user_id, chatname)
                        SELECT u.id, ?
                        FROM users u
                        WHERE u.username=?
                    """
            cursor.execute(query, (chatname, username))
            connection.commit()
            print("Чат создан")
            return True


def add_message(username, chatname, message):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        user_id = cursor.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()[0]
        chat_id = cursor.execute("SELECT id FROM chats WHERE chatname = ?", (chatname,)).fetchone()[0]
        cursor.execute("INSERT INTO messages (user_id, chat_id, message) VALUES (?, ?, ?)",
                       (user_id, chat_id, message,))
        connection.commit()


def delete_user(username):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        connection.commit()


def delete_chat(username, chatname):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        user_id = cursor.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()[0]
        chat_id = cursor.execute("SELECT id FROM chats WHERE chatname = ?", (chatname,)).fetchone()[0]
        cursor.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
        cursor.execute("DELETE FROM chats WHERE id = ?", (chat_id,))
        connection.commit()


def delete_message(username, chatname, message):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        user_id = cursor.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()[0]
        chat_id = cursor.execute("SELECT id FROM chats WHERE chatname = ?", (chatname,)).fetchone()[0]
        cursor.execute("DELETE FROM messages WHERE user_id = ? AND chat_id = ? AND message = ?",
                       (user_id, chat_id, message,))
        connection.commit()
