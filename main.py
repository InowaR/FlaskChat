import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from model.db import register_user, login_user

app = Flask(__name__, static_folder='static')
app.secret_key = 'qwerty'
app.permanent_session_lifetime = datetime.timedelta(minutes=10)


@app.route('/')
def get_home():
    return render_template('home.html')


@app.route('/profile/<message>', methods=['GET'])
def get_profile(message):
    username = session.get('username')
    return render_template('profile.html', username=username, message=message)


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
        message = 'Регистрация завершена'
        return redirect(url_for('get_profile', username=username, message=message))
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
        message = 'Вход выполнен'
        return redirect(url_for('get_profile', username=username, message=message))
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run()
