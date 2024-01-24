import datetime
from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_socketio import SocketIO, emit
from model.db import *
from model.game.service import Service
from model.utils.random_chat import *

app = Flask(__name__, static_folder='static')
app.secret_key = 'key'
app.permanent_session_lifetime = datetime.timedelta(minutes=30)
socketio = SocketIO(app)

poker = Service()


@app.route('/', methods=['GET'])
def get_list_chats():
    __login = session.get('login')
    if __login is None:
        return redirect(url_for('get_login'))
    list_chats = load_all_user_chats(__login)
    return render_template('list_chats.html', list_chats=list_chats)


@socketio.on("new_find_chat")
def find_chat(chatname: str):
    status = find_chat_by_name(chatname)
    if status:
        __login = session.get('login')
        message = chatname
        create_chat(chatname)
        status = is_user_in_chat(__login, chatname)
        if not status:
            add_user_to_chat(__login, chatname)
    else:
        message = ""
    emit("list_find_chats", message, broadcast=True)


@socketio.on("add_new_chat")
def add_chat(chatname: str):
    __login = session.get('login')
    status = create_chat(chatname)
    if status:
        add_user_to_chat(__login, chatname)
        message = "Создан новый чат"
    else:
        message = "Чат уже существует"
    emit("add_new_chat", message, broadcast=True)


@app.route('/add_new_chat', methods=['GET'])
def get_add_new_chat():
    __login = session.get('login')
    if __login is None:
        return redirect(url_for('get_login'))
    random_chats = find_all_chats()
    return render_template('add_new_chat.html', random_chats=random_chats)


@app.route('/chat', methods=['GET'])
def get_chat():
    __login = session.get('login')
    if __login is None:
        return redirect(url_for('get_login'))
    chatname = request.args.get('open_chat')
    if chatname is None:
        chatname = session.get('chatname')
    status = is_user_in_chat(__login, chatname)
    if not status:
        add_user_to_chat(__login, chatname)
    list_messages = load_all_messages_by_chat_name(chatname)
    return render_template('chat.html', chatname=chatname, list_messages=list_messages, login=__login)


@socketio.on("new_message")
def handle_new_message(chatname: str, message: str):
    __login = session.get('login')
    send_message(__login, chatname, message)
    emit("chat", {"login": __login, "message": message}, broadcast=True)


@app.route('/profile', methods=['GET'])
def get_profile():
    __login = session.get('login')
    if __login is None:
        return redirect(url_for('get_login'))
    return render_template('profile.html', login=__login)


@app.route('/register', methods=['GET'])
def get_register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    __login = request.form['login']
    password = request.form['password']
    status = register_new_user(__login, password)
    if status:
        session['login'] = __login
        session['password'] = password
        return redirect(url_for('get_profile'))
    else:
        message = "Пользователь уже существует"
        return render_template('register.html', message=message)


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    __login = request.form['login']
    password = request.form['password']
    status = check_user(__login, password)
    if status:
        session['login'] = __login
        session['password'] = password
        return redirect(url_for('get_profile'))
    else:
        message = "Пользователь не найден"
        return render_template('login.html', message=message)


@app.route('/logout', methods=['GET'])
def get_logout():
    session.clear()
    response = make_response(redirect(url_for('get_login')))
    response.delete_cookie('session')
    return response


@app.route('/delete_user', methods=['GET'])
def get_delete_user():
    __login = session.get('login')
    if __login is None:
        return redirect(url_for('get_login'))
    delete_user(__login)
    session.clear()
    response = make_response(redirect(url_for('get_login')))
    response.delete_cookie('session')
    return response


@app.route('/', methods=['POST'])
def get_delete_chat():
    __login = session.get('login')
    if __login is None:
        return redirect(url_for('get_login'))
    chatname = request.form['button-delete-chat']
    delete_chat(__login, chatname)
    return redirect(url_for('get_list_chats'))


@app.route('/chat', methods=['POST'])
def get_delete_message():
    if session.get('login') is None:
        return redirect(url_for('get_login'))
    button = request.form['button-delete-message']
    arr = button.split(',')
    __login = arr[0]
    chatname = arr[1]
    message = arr[2]
    session['chatname'] = chatname
    if __login == session['login']:
        delete_message(__login, chatname, message)
        return redirect(url_for('get_chat'))
    else:
        return redirect(url_for('get_chat'))


@app.route("/game", methods=["GET", "POST"])
def game():
    __login = session.get('login')
    if __login is None:
        return redirect(url_for('get_login'))
    print(__login)
    check = poker.check_players(__login)
    if not check:
        poker.add_new_player(__login)
    game_id = poker.add_new_playing_game()
    if not game_id:
        return render_template("game.html", message='Ожидайте игру')
    else:
        return redirect(url_for('play_game', game_id=game_id))


@app.route("/game/<game_id>", methods=["GET", "POST"])
def play_game(game_id: str):
    player1 = ''
    player2 = ''
    __login = session.get('login')
    print(__login)
    game_session = poker.find_game_by_id(game_id)
    for player in game_session.show_players():
        if player[0] == __login:
            player1 = player
        if player[0] != __login:
            player2 = player
    return render_template("game.html", game_id=game_id, login=__login, player1=player1, player2=player2, message='Игра началась!')


@socketio.on("get_button")
def get_button(message: str):
    game_id = message[0]
    player = message[1]
    button = message[2]
    game_session = poker.find_game_by_id(game_id)
    for player in game_session.show_players():
        print(player)
    emit("buttons", message, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)
