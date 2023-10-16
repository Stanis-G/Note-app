import os
from datetime import datetime
from flask import (
    Flask, render_template, url_for, request, g,
    flash, session, redirect, abort
)

from modules.note import Note
from modules.database import TableProfile, TableWritable
from modules.utils import set_menu, is_user_logged


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

# -----------------------------------------------------------------
# main menu buttons

# Main page
@app.route("/index")
@app.route("/")
def index(app_name=app.name):
    return render_template('index.html', app_name=app_name, title='Главная', menu=set_menu(), login=is_user_logged())


# Page with app description
@app.route("/about")
def about(app_name=app.name):
    """About handler"""
    return render_template("about.html", app_name=app_name, title="О сайте", menu=set_menu(), login=is_user_logged())


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
    return render_template('contact.html', title='Обратная связь', menu=set_menu(), login=is_user_logged())

# -----------------------------------------------------------------
# profile handlers (note, that some of them contain TableProfile)

@app.route("/login", methods=['POST', 'GET'])
def login():
    """Login page"""
    # Если свойство userLogged есть в нашей сессии (т.е. юзер залогинился)
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
    return render_template('login.html', title='Авторизация', menu=set_menu())

@app.route('/logout')
def logout():
    if 'userLogged' in session:
        session.pop('userLogged')
    return redirect(url_for('login'))


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
    return render_template('new_profile.html', title='Регистрация нового профиля', menu=set_menu())


# Username profile page
@app.route("/profile/<path:username>")
def profile(username, app_name=app.name):
    """User profile handler"""
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    notes = TableWritable('database.db', session['userLogged'])
    return render_template(
        "profile.html",
        app_name=app_name,
        title=f'Профиль: {username}',
        menu=set_menu(),
        login=is_user_logged(),
        notes=notes.get_all_notes(),
    )

# Error handler
@app.errorhandler(404)
def pageNotFound(error):
    """Not found (404) error handler"""
    return render_template('base.html', title='Указанной страницы не существует', menu=set_menu()), 404


# -----------------------------------------------------------------
# note handlers


@app.route('/new_note', methods=['POST', 'GET'])
def new_note():
    """Create new note page"""
    note_table = TableWritable('database.db', session['userLogged'])
    if request.method == 'GET':
        return render_template('new_note.html', title='Создание новой заметки', menu=set_menu(), login=is_user_logged())
    if request.method == 'POST':
        text = request.form['text']
        note = Note(session['userLogged'], request.form['header'])
        note.write(text)
        note_table.save_new(note)
        flash('Заметка создана', category='success')
        return redirect(url_for('profile', username=session['userLogged']))


@app.route('/note/<path:header>', methods=['POST', 'GET'])
def note(header):
    """Note page"""
    note_table = TableWritable('database.db', session['userLogged'])

    note_old = note_table.get_note(header)

    if request.method == 'GET':
        # Open existing note
        return render_template('note.html', title=header, menu=set_menu(), login=is_user_logged(), note=note_old)

    elif request.method == 'POST':
        # Change existing note
        
        # Take values from form
        header_new = request.form['header']
        text_new = request.form['text']

        # Create new note, which will replace existing one
        note_new = Note(session['userLogged'], header_new)
        note_new.write(text_new)
        note_new.set_meta(note_old.meta['creation_date'], str(datetime.now()).split('.')[0])
        
        # Update existing note data in the db
        note_table.update_existing(header_old=header, notebook_new=note_new)
        return render_template('note.html', title=header_new, menu=set_menu(), login=is_user_logged(), note=note_new)


@app.route('/delete/<path:header>', methods=['POST', 'GET'])
def delete(header):
    """Delete note page"""
    note_table = TableWritable('database.db', session['userLogged'])
    note_table.delete(header)
    return redirect(url_for('profile', username=session['userLogged']))






# Этот блок может остутствовать, а приложение будет запускаться из терминала
if __name__ == "__main__":
    app.run(debug=True)


# Создание тестового контекста запроса внутри контекста приложения app
# для проверки наличия переменной
# with app.test_request_context():
#   print(url_for('index'))




