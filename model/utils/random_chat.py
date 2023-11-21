import random
import sqlite3

db = 'model/site.db'


def find_all_chats():
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    SELECT chatname
                    FROM chats
                """
        cursor.execute(query)
        chats = [row[0] for row in cursor.fetchall()]
        random.shuffle(chats)
        return chats[:5]


def is_user_in_chat(login: str, chatname: str):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    SELECT login
                    FROM chat_users
                    WHERE login = ? AND chatname = ?
                """
        cursor.execute(query, (login, chatname))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False
