import os
from copy import copy
from flask import (
    Flask, render_template, url_for, request, g,
    flash, session, redirect, abort
)


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
        menu_new.append({'name': 'Выход', 'url': 'logout'})
    else:
        menu_new.append({'name': 'Вход', 'url': 'login'})
    return menu_new


# Main page
@app.route("/index")
@app.route("/")
def index(app_name=app.name):
    print(menu)
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



@app.route("/login", methods=['POST', 'GET'])
def login():

    # Если свойство userLogged есть в нашей сессии (т.е. юзер залогинился)
    if 'userLogged' in session:
        # то делаем переадресацию на профиль данного юзера
        return redirect(url_for('profile', username=session['userLogged']))
    # Если форма логина заполнена, то берем свойства (имя и пароль) оттуда
    elif request.method == 'POST' and request.form['username'] == 'selfedu' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=set_menu(menu))

@app.route('/logout')
def logout():
    if 'userLogged' in session:
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        session.pop('userLogged')
    return redirect(url_for('login'))

# Username profile page
@app.route("/profile/<path:username>")
def profile(username, app_name=app.name):
    """User profile handler"""
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    # Если пользователь не залогинен или имя юзера в текущей сессии не совпадает
    # с переданным именем юзера, то вывести ошибку 401
    # if 'userLogged' not in session or session['userLogged'] != username:
    #     abort(401)
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




