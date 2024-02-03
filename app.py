import os
from datetime import datetime
from flask import (
    Flask, render_template, url_for, request, g,
    flash, session, redirect, abort
)

from modules.note import Note
from modules.database import TableNotes
from modules.utils import set_menu
from handlers.profile import profile_print


# Config variables
DATABASE = 'database.db' # Путь к БД
DEBUG = True # Режим отладки
SECRET_KEY = 'ghn2fdngssfis232dnfios253nfonsd'

app = Flask(__name__)
app.register_blueprint(profile_print)

# Присваиваем приложению случайный секретный ключ
# Используется для шифрования вводимых пользователем данных
# app.config['SECRET_KEY'] = 'ghn2fdngssfis232dnfios253nfonsd'
app.config.from_object(__name__) # Загружаем конфигурационные переменные
# Переопределим путь к БД
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))

# -----------------------------------------------------------------
# main menu pages

# Main page
@app.route("/main")
@app.route("/")
def main(app_name=app.name):
    """Main page with icons of app sections"""
    return render_template('main.html', app_name=app_name, title='Главная', menu=set_menu(), username=session.get('username'))


# Page with app description
@app.route("/about")
def about(app_name=app.name):
    """About page handler"""
    return render_template("about.html", app_name=app_name, title="О сайте", menu=set_menu(), username=session.get('username'))


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    """Contact form handler"""

    if request.method == 'POST':

        # Preliminary checks
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:   
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', title='Обратная связь', menu=set_menu(), username=session.get('username'))


# Error handler
@app.errorhandler(404)
def pageNotFound(error):
    """Not found (404) error handler"""
    return render_template('base.html', title='Указанной страницы не существует', menu=set_menu()), 404


# -----------------------------------------------------------------
# note handlers

@app.route("/profile/<path:username>/notes")
def notes(username):
    """User profile handler"""
    print(username)
    if 'username' not in session or session['username'] != username:
        abort(401)
    
    notes = TableNotes('database.db', session['username'])
    return render_template(
        "notes.html",
        title='Заметки',
        menu=set_menu(),
        username=session.get('username'),
        notes=notes.get_all_notes(),
    )


@app.route('/new_note', methods=['POST', 'GET'])
def new_note():
    """Create new note page"""

    note_table = TableNotes('database.db', session['username'])
    if request.method == 'GET':
        return render_template('new_note.html', title='Создание новой заметки', menu=set_menu(), username=session.get('username'))
    
    if request.method == 'POST':
        text = request.form['text']
        note = Note(session['username'], request.form['header'])
        note.write(text)
        print(note.owner, note.header)
        note_table.save_note(note)
        return redirect(url_for('notes', username=session['username']))


@app.route('/note/<path:header>', methods=['POST', 'GET'])
def note(header):
    """Note page"""
    note_table = TableNotes('database.db', session['username'])

    note_old = note_table.get_note_by_header(header)

    if request.method == 'GET':
        # Open existing note
        return render_template('note.html', title=header, menu=set_menu(), username=session.get('username'), note=note_old)

    elif request.method == 'POST':
        # Change existing note
        
        # Take values from form
        header_new = request.form['header']
        text_new = request.form['text']

        # Create new note, which will replace existing one
        params = dict(
            header=header_new,
            creation_date=note_old.creation_date,
            last_change_date=str(datetime.now()).split('.')[0],
            owner=note_old.owner,
            content=note_old.content,
        )
        note_new = Note.restore_from_db(params)
        note_new.write(text_new)
        
        # Update existing note in db
        note_table.update_note(header_old=header, note_new=note_new)

        return render_template('note.html', title=header_new, menu=set_menu(), username=session.get('username'), note=note_new)
    

@app.route("/profile/<path:username>/lectures")
def lectures(username):
    """User profile handler"""

    if 'username' not in session or session['username'] != username:
        abort(401)
    
    notes = TableNotes('database.db', session['username'])
    return render_template(
        "lectures.html",
        title='Лекции',
        menu=set_menu(),
        username=session.get('username'),
        notes=lectures.get_all_notes(),
    )
    

@app.route('/lecture/<path:header>', methods=['POST', 'GET'])
def lecture(header):
    """Note page"""
    note_table = TableNotes('database.db', session['username'])

    note_old = note_table.get_note_by_header(header)

    if request.method == 'GET':
        # Open existing note
        return render_template('lecture.html', title=header, menu=set_menu(), username=session.get('username'), note=note_old)

    elif request.method == 'POST':
        # Change existing note
        
        # Take values from form
        header_new = request.form['header']
        text_new = request.form['text']

        # Create new note, which will replace existing one
        params = dict(
            header=header_new,
            creation_date=note_old.creation_date,
            last_change_date=str(datetime.now()).split('.')[0],
            owner=note_old.owner,
            content=note_old.content,
        )
        note_new = Note.restore_from_db(params)
        note_new.write(text_new)
        
        # Update existing note in db
        note_table.update_note(header_old=header, note_new=note_new)

        return render_template('lecture.html', title=header_new, menu=set_menu(), username=session.get('username'), note=note_new)
    

@app.route("/profile/<path:username>/calendar")
def calendar(username):
    """User profile handler"""

    if 'username' not in session or session['username'] != username:
        abort(401)
    
    notes = TableNotes('database.db', session['username'])
    return render_template(
        "calendar.html",
        title='Заметки',
        menu=set_menu(),
        username=session.get('username'),
        notes=notes.get_all_notes(),
    )


@app.route('/delete/<path:header>', methods=['POST', 'GET'])
def delete(header):
    """Delete note page"""
    note_table = TableNotes('database.db', session['username'])
    note_table.delete(header)
    return redirect(url_for('notes', username=session['username']))






# Этот блок может остутствовать, а приложение будет запускаться из терминала
if __name__ == "__main__":
    app.run(debug=True)


# Создание тестового контекста запроса внутри контекста приложения app
# для проверки наличия переменной
# with app.test_request_context():
#   print(url_for('main'))




