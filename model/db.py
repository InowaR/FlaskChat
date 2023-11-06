import sqlite3

db = 'users.db'


def create_db():
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username text, password text)''')
        conn.commit()


def register_user(username: str, password: str):
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username, ))
        user = c.fetchone()

    if user:
        return False
    else:
        with sqlite3.connect(db) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
        return True


def login_user(username: str, password: str):
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

    if user:
        return True
    else:
        return False
