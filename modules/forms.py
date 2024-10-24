from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    message = StringField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class LoginForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class NewProfileForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_check = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Создать')


class NewNoteForm(FlaskForm):
    header = StringField('Название', validators=[DataRequired()])
    text = TextAreaField('Текст')
    submit = SubmitField('Сохранить')


class NoteForm(FlaskForm):
    header = StringField('Название', validators=[DataRequired()])
    text = TextAreaField('Текст')
    submit = SubmitField('Сохранить')
