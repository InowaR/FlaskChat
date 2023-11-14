import datetime
from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_socketio import SocketIO, emit
from model.db import *

app = Flask(__name__, static_folder='static')
app.secret_key = 'key'
app.permanent_session_lifetime = datetime.timedelta(minutes=30)
socketio = SocketIO(app)


@app.route('/', methods=['GET'])
def get_list_chats():
    if session.get('username') is None:
        return redirect(url_for('get_login'))
    pass
    # username = session.get('username')
    # list_chats = load_all_user_chats(username)
    # return render_template('list_chats.html', list_chats=list_chats)


@socketio.on("new_find_chat")
def find_chat(chat_name: str):
    pass
    # status = find_chat_by_name(chat_name)
    # if status:
    #     emit("list_find_chats", chat_name, broadcast=True)


@socketio.on("add_new_chat")
def add_chat(chat_name: str):
    created_by = session.get('username')
    # status = create_new_chat(chat_name, created_by)
    # if status:
    #     message = "Создан новый чат"
    # else:
    #     message = "Чат уже существует"
    # emit("add_new_chat", message, broadcast=True)


@app.route('/add_new_chat', methods=['GET'])
def get_add_new_chat():
    return render_template('add_new_chat.html')


@app.route('/chat', methods=['GET'])
def get_chat():
    if session.get('username') is None:
        return redirect(url_for('get_login'))
    chat_name = request.args.get('open_chat')
    # list_messages = load_all_messages_by_chat_name(chat_name)
    # return render_template('chat.html', chat_name=chat_name, list_messages=list_messages)


@socketio.on("new_message")
def handle_new_message(chat_name, message: str):
    pass
    # username = session.get('username')
    # time = datetime.datetime.now()
    # print(f"New message: {chat_name}, {username} {time} {message}")
    # add_new_message_to_chat(chat_name, username, time, message)
    # emit("chat", {"username": username, "message": message}, broadcast=True)


@app.route('/profile', methods=['GET'])
def get_profile():
    if session.get('username') is None:
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
    status = register_new_user(username, password)
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
    status = check_user(username, password)
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
