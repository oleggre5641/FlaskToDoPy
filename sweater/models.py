from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate(db)


class Notes(db.Model):
    """
        Модель заметок
        Создание столбцов в таблице
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text_uno = db.Column(db.String(100), nullable=False)
    text_dos = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    uid = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        # Выдача объекта и айди
        return "<Notes %r>" % self.id


class User (db.Model, UserMixin):
    """
    Модель пользователей
    Создание столбцов в таблице
    """
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
