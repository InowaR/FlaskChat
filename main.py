import datetime
from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_socketio import SocketIO, emit
from model.db import register_user, login_user

app = Flask(__name__, static_folder='static')
app.secret_key = 'key'
app.permanent_session_lifetime = datetime.timedelta(seconds=10)
socketio = SocketIO(app)


@app.route('/', methods=['GET'])
def get_home():
    if session.get('username') is None:
        return redirect(url_for('get_login'))
    return render_template('home.html')


@socketio.on("new_message")
def handle_new_message(message):
    username = session['username']
    print(f"New message: {username} : {message}")
    emit("chat", {"username": username, "message": message}, broadcast=True)


@app.route('/profile', methods=['GET'])
def get_profile():
    session_id = request.cookies.get('session')
    if session_id is None:
        return redirect(url_for('get_login'))
    username = session.get('username')
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
        return redirect(url_for('get_profile'))
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    status = login_user(username, password)
    if status:
        session['username'] = username
        session['password'] = password
        return redirect(url_for('get_profile'))
    else:
        return render_template('login.html')


@app.route('/logout')
def get_logout():
    session.clear()
    response = make_response(redirect(url_for('get_login')))
    response.delete_cookie('session')
    return response


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
