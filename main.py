from flask import Flask, request, render_template

app = Flask(__name__)


def save_data(file, data):
    with open(file, 'a') as f:
        f.write(f'{data}\n')


@app.route('/', methods=['GET'])
def index_html():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_form():
    if 'name' in request.form:
        name = request.form['name']
        save_data('name.txt', name)
        return render_template('index.html', message1='Name saved')
    if 'age' in request.form:
        age = request.form['age']
        save_data('age.txt', age)
        return render_template('index.html', message2='Age saved')


if __name__ == '__main__':
    app.run()
