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
def check_game():
    __login = session.get('login')
    if __login is None:
        return redirect(url_for('get_login'))
    check = poker.check_players(__login)
    if not check:
        poker.add_new_player(__login)
    game_id = poker.add_new_playing_game()
    find_new_game_id = poker.redirect_to_the_game(__login)
    if find_new_game_id:
        print(type(find_new_game_id))
        print(f'Найдена игра {find_new_game_id}')
        return redirect(url_for('play_game', game_id=find_new_game_id))
    # print(fin)
    print('Игра не найдена')
    # print(game_id)
    # print(poker.show_players(game_id))
    if not game_id:
        return render_template("game.html", game_id=False, message='Ожидайте игру')
    else:
        return redirect(url_for('play_game', game_id=game_id))


@app.route("/game/<game_id>", methods=["GET", "POST"])
def play_game(game_id: str):
    player1 = ''
    player2 = ''
    __login = session.get('login')
    for player in poker.show_players(game_id):
        if player[0] == __login:
            player1 = player
        if player[0] != __login:
            player2 = player
    if poker.find_game_by_id(game_id):
        time_now = datetime.datetime.now()
        time_start_game = poker.get_time_game_start(game_id)
        delta = time_now - time_start_game
        # print(delta.total_seconds() > 3)
        if poker.check_end_game(game_id):
            print('игра окончена')
            # poker.delete_game(game_id)
            # for p in poker.list_playing_games:
            #     print(p.game_id)
            return render_template("game.html", game_id=game_id, login=__login,
                                   player1=player1, player2=player2, buttons=1, message='Игра окончена')
        if poker.check_player_money(game_id, __login):
            no_raise = 1
        else:
            no_raise = 0
        table_money = poker.show_table_money(game_id)
        group_round = poker.check_group_round(game_id)
        preflop_status, flop_status, turn_status, river_status = poker.check_player_buttons(game_id, __login)
        if 0 <= group_round < 2:
            b1, b2 = poker.blind(game_id)
            poker.preflop(game_id)
            if preflop_status:
                return render_template("game.html", game_id=game_id, login=__login,
                                       b1=b1, b2=b2, player1=player1, player2=player2,
                                       player_round=0, buttons=1, table_money=table_money)
            else:
                return render_template("game.html", game_id=game_id, login=__login,
                                       b1=b1, b2=b2, player1=player1, player2=player2,
                                       player_round=0, buttons=0, no_raise=no_raise, table_money=table_money)
        if 2 <= group_round < 4:
            flop_cards = poker.flop(game_id)
            if flop_status:
                return render_template("game.html", game_id=game_id, login=__login,
                                       player1=player1, player2=player2, player_round=1, buttons=1,
                                       table_cards=flop_cards, table_money=table_money)
            else:
                return render_template("game.html", game_id=game_id, login=__login,
                                       player1=player1, player2=player2, player_round=1, buttons=0,
                                       table_cards=flop_cards, no_raise=no_raise, table_money=table_money)
        if 4 <= group_round < 6:
            turn_cards = poker.turn(game_id)
            if turn_status:
                return render_template("game.html", game_id=game_id, login=__login,
                                       player1=player1, player2=player2, player_round=2, buttons=1,
                                       table_cards=turn_cards, table_money=table_money)
            else:
                return render_template("game.html", game_id=game_id, login=__login,
                                       player1=player1, player2=player2, player_round=2, buttons=0,
                                       table_cards=turn_cards, no_raise=no_raise, table_money=table_money)
        if 6 <= group_round < 8:
            river_cards = poker.river(game_id)
            if river_status:
                return render_template("game.html", game_id=game_id, login=__login,
                                       player1=player1, player2=player2, player_round=3, buttons=1,
                                       table_cards=river_cards, table_money=table_money)
            else:
                return render_template("game.html", game_id=game_id, login=__login,
                                       player1=player1, player2=player2, player_round=3, buttons=0,
                                       table_cards=river_cards, no_raise=no_raise, table_money=table_money)
        if group_round >= 8:
            poker.new_deal(game_id)
            return render_template("game.html", game_id=game_id, login=__login,
                                   player1=player1, player2=player2, buttons=1, table_money=table_money)


@socketio.on("get_button")
def get_button(message: str):
    game_id, player_name, button, player_round = message
    if poker.find_game_by_id(game_id):
        poker.press_button(game_id, player_name, button, player_round)
        # print(game_id, player_name, button, player_round)


if __name__ == '__main__':
    socketio.run(app, use_reloader=True, log_output=True, allow_unsafe_werkzeug=True)
