from . import db
from flask_login import UserMixin
from datetime import datetime

# Таблица пользователей
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False) # Логин для входа
    display_name = db.Column(db.String(50)) # Ник в чате
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    bio = db.Column(db.String(500))
    followers_count = db.Column(db.Integer, default=0)
    
    # Логика бана и мута
    is_banned = db.Column(db.Boolean, default=False)
    muted_until = db.Column(db.DateTime, nullable=True)

# Таблица инвайтов
class Invite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True)
    is_used = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

# Таблица ачивок
class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    image_url = db.Column(db.String(200))

# Связь юзеров и ачивок (Многие ко многим)
user_achievements = db.Table('user_achievements',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('achievement_id', db.Integer, db.ForeignKey('achievement.id'))
)