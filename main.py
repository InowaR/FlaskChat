import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from model.db import register_user, login_user

app = Flask(__name__, static_folder='static')
app.secret_key = 'key'
app.permanent_session_lifetime = datetime.timedelta(minutes=1)
socketio = SocketIO(app)


@app.route('/', methods=['GET'])
def get_home():
    return render_template('home.html')


@socketio.on("new_message")
def handle_new_message(message):
    print(request.sid)
    print(f"New message: {message}")
    emit("chat", {"message": message, "username": request.sid}, broadcast=True)


@app.route('/profile', methods=['GET'])
def get_profile():
    username = session.get('username')
    print(session)
    return render_template('profile.html', username=username)


@app.route('/register', methods=['GET'])
def get_register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    status = register_user(username, password)
    if status:
        session['username'] = username
        session['password'] = password
        print(session.get('username'), session.get('password'))
        return redirect(url_for('get_profile', username=username))
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(session.get('username'), session.get('password'))
    status = login_user(username, password)
    if status:
        session['username'] = username
        session['password'] = password
        return redirect(url_for('get_profile', username=username))
    else:
        return render_template('login.html')


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
