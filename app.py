import os
from copy import copy
from flask import (
    Flask, render_template, url_for, request, g,
    flash, session, redirect, abort
)

from modules.database import TableProfile


# Конфигурационные переменные (обычно пишутся заглавными буквами)
DATABASE = 'database.db' # Путь к БД
DEBUG = True # Режим отладки
SECRET_KEY = 'ghn2fdngssfis232dnfios253nfonsd'

app = Flask(__name__)

# Присваиваем приложению случайный секретный ключ
# Используется для шифрования вводимых пользователем данных
# app.config['SECRET_KEY'] = 'ghn2fdngssfis232dnfios253nfonsd'
app.config.from_object(__name__) # Загружаем конфигурационные переменные
# Переопределим путь к БД
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))

menu = [
    {'name': 'Главная', 'url': '/index'},
    {'name': 'О приложении', 'url': '/about'},
    {'name': 'Обратная связь', 'url': '/contact'},
]

def set_menu(menu):
    menu_new = copy(menu)
    if 'userLogged' in session:
        menu_new.append({'name': 'Выход', 'url': '/logout'})
    else:
        menu_new.append({'name': 'Вход', 'url': '/login'})
    return menu_new


# Main page
@app.route("/index")
@app.route("/")
def index(app_name=app.name):
    return render_template('index.html', app_name=app_name, title='Главная', menu=set_menu(menu))


# Page with app description
@app.route("/about")
def about(app_name=app.name):
    """About handler"""
    return render_template("about.html", app_name=app_name, title="О сайте", menu=set_menu(menu))


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    """Contact form handler"""
    if request.method == 'POST':
        # Добавляем мгновенное сообщение
        # category нужен для правильного выбора стилей
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:   
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', title='Обратная связь', menu=set_menu(menu))


@app.route("/new_profile", methods=['POST', 'GET'])
def new_profile():
    """Create new profile page"""
    profiles = TableProfile('database.db')
    if request.method == 'POST':
        if request.form['new_psw'] == request.form['psw_check']:
            login = request.form['new_username']
            psw = request.form['new_psw']
            profiles.create_profile(login, psw)
            flash('Профиль создан', category='success')
        else:
            flash('Пароли не совпадают', category='error')
    return render_template('new_profile.html', title='Регистрация нового профиля', menu=set_menu(menu))


@app.route("/login", methods=['POST', 'GET'])
def login():
    """Login page"""
    # Если свойство userLogged есть в нашей сессии (т.е. юзер залогинился)
    #print(request.form[''])
    profiles = TableProfile('database.db')
    if 'userLogged' in session:
        # то делаем переадресацию на профиль данного юзера
        return redirect(url_for('profile', username=session['userLogged']))
    # Если форма логина заполнена, то берем свойства (имя и пароль) оттуда
    if request.method == 'POST':
        if request.form['username'] in profiles.get_logins() and request.form['psw'] == profiles.get_profile(request.form['username'])['password']:
            session['userLogged'] = request.form['username']
            return redirect(url_for('profile', username=session['userLogged']))
        elif request.form['username'] not in profiles.get_logins():
            flash('Неверно указано имя пользователя или пароль', category='error')
        elif request.form['username'] in profiles.get_logins() and request.form['psw'] != profiles.get_profile(request.form['username'])['password']:
            flash('Неверно указано имя пользователя или пароль', category='error')
    return render_template('login.html', title='Авторизация', menu=set_menu(menu))

@app.route('/logout')
def logout():
    if 'userLogged' in session:
        session.pop('userLogged')
    return redirect(url_for('login'))

# Username profile page
@app.route("/profile/<path:username>")
def profile(username, app_name=app.name):
    """User profile handler"""
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return render_template("profile.html", app_name=app_name, title=f'Профиль: {username}', menu=set_menu(menu))

# Error handler
@app.errorhandler(404)
def pageNotFound(error):
    """Not found (404) error handler"""
    return render_template('base.html', title='Указанной страницы не существует', menu=set_menu(menu)), 404

# Этот блок может остутствовать, а приложение будет запускаться из терминала
if __name__ == "__main__":
    app.run(debug=True)


# Создание тестового контекста запроса внутри контекста приложения app
# для проверки наличия переменной
# with app.test_request_context():
#   print(url_for('index'))




