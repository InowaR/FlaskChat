from flask import Flask, render_template, request
from model.db import register_user, login_user

app = Flask(__name__)


@app.route('/profile', methods=['GET'])
def get_profile():
    return render_template('profile.html')


@app.route('/register', methods=['GET'])
def get_register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    status = register_user(username, password)
    if status:
        message = 'Регистрация завершена'
        return render_template('profile.html', username=username, message=message)
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
        message = 'Вход выполнен'
        return render_template('profile.html', username=username, message=message)
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run()
