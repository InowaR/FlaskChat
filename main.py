from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

db = 'users.db'


def create_db():
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username text, password text)''')
        conn.commit()


@app.route('/register', methods=['GET'])
def get_register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", username)
        user = c.fetchone()

    if user:
        return 'Username already taken'
    else:
        with sqlite3.connect(db) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
        return f'User {username} registered successfully'


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    with sqlite3.connect(db) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

    if user:
        return f'Welcome {username}'
    else:
        return 'Invalid username or password'


if __name__ == '__main__':
    app.run()
