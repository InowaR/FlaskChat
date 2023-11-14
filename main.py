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
    username = session.get('username')
    list_chats = load_all_user_chats(username)
    return render_template('list_chats.html', list_chats=list_chats)


@socketio.on("new_find_chat")
def find_chat(chatname: str):
    status = find_chat_by_name(chatname)
    if status:
        username = session.get('username')
        message = chatname
        create_new_chat(username, chatname)
    else:
        message = ""
    emit("list_find_chats", message, broadcast=True)


@socketio.on("add_new_chat")
def add_chat(chatname: str):
    username = session.get('username')
    status = create_new_chat(username, chatname)
    if status:
        message = "Создан новый чат"
    else:
        message = "Чат уже существует"
    emit("add_new_chat", message, broadcast=True)


@app.route('/add_new_chat', methods=['GET'])
def get_add_new_chat():
    return render_template('add_new_chat.html')


@app.route('/chat', methods=['GET'])
def get_chat():
    if session.get('username') is None:
        return redirect(url_for('get_login'))
    username = session.get('username')
    chatname = request.args.get('open_chat')
    list_messages = load_all_messages_by_chat_name(username, chatname)
    return render_template('chat.html', chatname=chatname, list_messages=list_messages)


@socketio.on("new_message")
def handle_new_message(chatname: str, message: str):
    username = session.get('username')
    print(f"New message: {username}, {chatname} {message}")
    add_new_message_to_chat(username, chatname, message)
    emit("chat", {"username": username, "message": message}, broadcast=True)


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


@app.route('/logout', methods=['GET'])
def get_logout():
    session.clear()
    response = make_response(redirect(url_for('get_login')))
    response.delete_cookie('session')
    return response


@app.route('/delete_user', methods=['GET'])
def get_delete_user():
    username = session.get('username')
    delete_user(username)
    session.clear()
    response = make_response(redirect(url_for('get_login')))
    response.delete_cookie('session')
    return response


@app.route('/', methods=['POST'])
def get_delete_chat():
    name = request.form['button']
    print(name)
    # delete_chat(chatname)
    return redirect(url_for('get_profile'))


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
