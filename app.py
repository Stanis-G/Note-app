import os
from dotenv import load_dotenv
from datetime import datetime
from flask import (
    Flask, render_template, url_for, request, g,
    flash, session, redirect, abort
)

from modules.database import NoteCollection, LectureCollection
from modules.forms import NewNoteForm
from modules.note import Note
from modules.utils import set_menu
from handlers.profile import profile_print


load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
# DEBUG = os.getenv("DEBUG")
# SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.register_blueprint(profile_print)

# Присваиваем приложению случайный секретный ключ
# Используется для шифрования вводимых пользователем данных
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['DEBUG'] = os.getenv("DEBUG")
app.config.from_object(__name__) # Загружаем конфигурационные переменные
# Переопределим путь к БД
# app.config.update(dict(DATABASE=os.path.join(app.root_path, DATABASE)))

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
    return render_template('header.html', title='Указанной страницы не существует', menu=set_menu()), 404


# -----------------------------------------------------------------
# note handlers

@app.route("/profile/<path:username>/notes")
def notes(username):
    """Note page with notes preview"""
    print(username)
    if 'username' not in session or session['username'] != username:
        abort(401)
    
    db = NoteCollection(MONGO_URI, MONGO_DB, session['username'])
    with db:
        notes = db.read_all()
    return render_template(
        "notes.html",
        title='Заметки',
        menu=set_menu(),
        username=session.get('username'),
        notes=notes,
    )


@app.route('/new_note', methods=['POST', 'GET'])
def new_note():
    """Create new note page"""

    form = NewNoteForm()

    if request.method == 'GET':
        return render_template('new_note.html', title='Создание новой заметки', menu=set_menu(), username=session.get('username'), form=form)
    
    if request.method == 'POST':
        note = dict(
            user=session['username'],
            header=request.form['header'],
            text=request.form['text'],
        )
        db = NoteCollection(MONGO_URI, MONGO_DB, session['username'])
        with db:
            db.create_record(note)
        if form.validate_on_submit():
            return redirect(url_for('notes', username=session['username']))
        else:
            pass # Need to raise some error


@app.route('/note/<path:header>', methods=['POST', 'GET'])
def note(header):
    """Note page"""

    db = NoteCollection(MONGO_URI, MONGO_DB, session['username'])
    with db:
        note_old = db.read_record_by_name(header)

        if request.method == 'GET':
            # Open existing note
            return render_template('note.html', title=header, menu=set_menu(), username=session.get('username'), note=note_old)

        elif request.method == 'POST':
            # Change existing note

            # Create new note with updated data
            note_new = note_old
            note_new.update(request.form)
        
        # Update existing note in db
        db.update_record_by_name(header, note_new)

        return render_template('note.html', title=note_new['header'], menu=set_menu(), username=session.get('username'), note=note_new)


@app.route('/delete/<path:header>')
def delete(header):
    """Delete note page"""

    db = NoteCollection(MONGO_URI, MONGO_DB, session['username'])
    with db:
        db.delete_record_by_name(header)
    return redirect(url_for('notes', username=session['username']))


# -----------------------------------------------------------------
# lecture handlers

@app.route("/profile/<path:username>/lectures")
def lectures(username):
    """Страница-заглушка"""
    return '''<html>Заглушка</html>'''


@app.route("/profile/<path:username>/calendar")
def calendar(username):
    """Страница-заглушка"""
    return '''<html>Заглушка</html>'''
