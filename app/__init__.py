import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Инициализируем объекты, но не привязываем к приложению сразу
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login' # Куда кидать юзера, если он не вошел

def create_app():
    load_dotenv(os.path.join(os.path.dirname(__file__), '../secrets/.env'))
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev_key')
    
    # Настройки БД
    db_user = os.getenv('POSTGRES_USER')
    db_pass = os.getenv('POSTGRES_PASSWORD')
    db_host = 'db'
    db_name = os.getenv('POSTGRES_DB')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    # Импортируем маршруты и модели ВНУТРИ функции, чтобы избежать циклического импорта
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app