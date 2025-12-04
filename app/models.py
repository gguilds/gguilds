'''Модели данных'''
from datetime import datetime, timezone
from typing import Optional
from hashlib import md5

from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin

from app import db
from app import login


@login.user_loader
def load_user(user_id):
    '''Загрузчик пользователя'''
    return db.session.get(User, int(user_id))

class User(UserMixin, db.Model):
    '''Пользователь'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        '''Задать пароль'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''Проверить пароль'''
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        '''Аватар из gravatar'''
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

class Post(db.Model):
    '''Посты'''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return f'<Post {self.body}>'
