import sqlite3

db = 'model/site.db'


def delete_old_chats():
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    DELETE
                    FROM chats
                    WHERE created_at < CURRENT_TIMESTAMP - INTERVAL 1 DAY;
                """
        cursor.execute(query)
        connection.commit()


def delete_old_messages():
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    DELETE
                    FROM messages
                    WHERE created_at < CURRENT_TIMESTAMP - INTERVAL 1 DAY;
                """
        cursor.execute(query)
        connection.commit()


def delete_all_messages():
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = """
                    DELETE FROM messages;
                """
        cursor.execute(query)
        connection.commit()
