import os
from dotenv import load_dotenv

from flask import (
    Blueprint, render_template, url_for, request, g,
    flash, session, redirect, abort
)

from modules.database import Profiles
from modules.forms import LoginForm, NewProfileForm
from modules.utils import set_menu

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")


profile_print = Blueprint(
    name='profile',
    import_name=__name__,
    template_folder='templates',
)


@profile_print.route("/login", methods=['POST', 'GET'])
def login():
    """Login page"""

    # Check if user is logged
    if 'username' in session:
        return redirect(url_for('profile.login', username=session['username']))
    
    form = LoginForm()

    if request.method == 'POST':

        db = Profiles(MONGO_URI, MONGO_DB)
        with db:

            # Check if username and password are correct
            usernames = [user['username'] for user in db.read_all()]
            is_user_found = request.form['username'] in usernames
            user_psw = db.read_record_by_name(request.form['username'])['password']
            is_psw_match_user = request.form['password'] == user_psw
            is_user_data_correct = is_user_found and is_psw_match_user
        if is_user_data_correct and form.validate_on_submit():
            session['username'] = request.form['username']
            return redirect(url_for('profile.profile', username=session['username']))
        else:
            flash('Неверно указано имя пользователя или пароль', category='error')

    return render_template('login.html', title='Авторизация', menu=set_menu(), form=form)


@profile_print.route('/logout')
def logout():
    """Quit profile"""

    if 'username' in session:
        session.pop('username')

    return redirect(url_for('profile.login'))


@profile_print.route("/new_profile", methods=['POST', 'GET'])
def new_profile():
    """Create new profile page"""

    form = NewProfileForm()

    if request.method == 'POST':

        if request.form['password'] == request.form['password_check']:
            db = Profiles(MONGO_URI, MONGO_DB)
            with db:
                profile = dict(
                    email=request.form['email'],
                    username=request.form['username'],
                    password=request.form['password'],
                )
                db.create_record(profile)
            if form.validate_on_submit():
                flash('Профиль создан', category='success')
                redirect(url_for('profile.login'))
        else:
            flash('Пароли не совпадают', category='error')

    return render_template('new_profile.html', title='Регистрация нового профиля', menu=set_menu(), form=form)


@profile_print.route("/profile/<path:username>")
def profile(username):
    """User profile handler"""

    if 'username' not in session or session['username'] != username:
        abort(401)

    return render_template(
        "profile.html",
        title=f'Профиль: {username}',
        menu=set_menu(),
        username=session.get('username'),
    )
