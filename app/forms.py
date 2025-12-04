'''Формы'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
    '''Форма авторизации'''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    '''Форма регистрации'''
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        '''Проверка имени пользователя'''
        query = sa.select(User).where(User.username == username.data)
        user = db.session.scalar(query)
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        '''Проверка email'''
        query = sa.select(User).where(User.email == email.data)
        user = db.session.scalar(query)
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    '''Форма изменения профиля'''
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
