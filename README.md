# Проект "Чат знакомств и игра в покер на Flask"
## Описание:
Данный проект представляет собой веб-сайт на Flask, который реализует функции чата знакомств и игры в покер. Пользователи могут регистрироваться, авторизоваться, создавать чаты, искать чаты, сохранять просмотренные чаты, сохранять историю сообщений, удалять сообщения.
## Функционал:
### Регистрация/авторизация:
* Пользователи могут регистрироваться, используя логин и пароль.
* Авторизация с помощью логина и пароля.
### Чаты:
* Создание чатов.
* Поиск чатов по названию.
* Сохранение просмотренных чатов.
* Обмен сообщениями в чатах.
* Сохранение истории сообщений.
* Удаление сообщений.
### Игра в покер:
* Возможность сыграть в покер со случайным игроком, который находится в комнате ожидания.
* Реализация игры в покер с использованием стандартных правил.
## Установка:
### Клонируйте репозиторий.
* Создайте виртуальное окружение: python3 -m venv .venv
* Активируйте виртуальное окружение: source .venv/bin/activate
* Установите зависимости: pip install -r requirements.txt
* Запустите приложение: main.py
* Доступ к приложению: Приложение будет доступно по адресу: http://localhost:5000
## Использование:
* Для регистрации/авторизации перейдите на страницу /register.
* Для создания чата перейдите на страницу /add_new_chat.
* Для поиска чатов перейдите на страницу /.
* Для входа в чат перейдите по ссылке на чат.
* Для игры в покер перейдите на страницу /game.
## Примечания:
Приложение находится в стадии разработки, и его функционал может быть расширен в будущем.