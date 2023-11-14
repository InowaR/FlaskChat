import sqlite3

db = 'model/site.db'


def create_db():
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """
        )
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    chatname TEXT NOT NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """
        )
        cursor.execute(
            """ CREATE TABLE IF NOT EXISTS messages (
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
        query = """ SELECT
                        chats.id,
                        chats.chatname,
                        users.username
                    FROM
                        chats
                    INNER JOIN users ON chats.user_id = users.id
                    WHERE
                        chats.chatname=? AND users.username=?;
                """
        cursor.execute(query, (chatname, username))
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


def find_chat_by_name(chatname: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM chats WHERE chatname=?", (chatname,))
        chat = cursor.fetchone()
        if chat:
            print("Чат существует")
            return True
        else:
            print("Чат не найден")
            return False


def load_all_messages_by_chat_name(username: str, chatname: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user_id = cursor.fetchone()[0]
        query = """ SELECT u.username, m.message
                    FROM messages m
                    INNER JOIN users u ON m.user_id = u.id
                    INNER JOIN chats c ON m.chat_id = c.id
                    WHERE c.chatname=? AND c.user_id=?
                    ORDER BY m.created_at ASC;
                """
        cursor.execute(query, (chatname, user_id))
        return cursor.fetchall()


def add_new_message_to_chat(username, chatname, message):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """ INSERT INTO messages (user_id, chat_id, message)
                    SELECT u.id, c.id, ?
                    FROM users u
                    INNER JOIN chats c ON u.username=? AND c.chatname=?;
                    """
        cursor.execute(query, (message, username, chatname))
        connection.commit()


def delete_user(username):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        connection.commit()


def delete_chat(chatname: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        list_chat_id = cursor.execute("SELECT id FROM chats WHERE chatname=?", (chatname,)).fetchall()
        for chat_id in list_chat_id:
            cursor.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id[0],))
            cursor.execute("DELETE FROM chats WHERE id=?", (chat_id[0],))
            connection.commit()


def delete_message(username: str, chatname: str, message: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        user_id = cursor.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()[0]
        list_chat_id = cursor.execute("SELECT id FROM chats WHERE chatname = ?", (chatname,)).fetchall()
        query = """ DELETE
                    FROM messages
                    WHERE user_id = ? AND chat_id = ? AND message = ?;
                """
        for chat_id in list_chat_id:
            cursor.execute(query, (user_id, chat_id[0], message,))
        connection.commit()
