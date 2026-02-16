import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Инициализируем объекты, но не привязываем к приложению сразу
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login' # Куда кидать юзера, если он не вошел

def create_app(test_config=None):
    load_dotenv(os.path.join(os.path.dirname(__file__), '../secrets/.env'))
    
    app = Flask(__name__)
    
    # Дефолтные настройки
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev_key')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config is None:
        # Если НЕ тест — берем Postgres
        db_user = os.getenv('POSTGRES_USER')
        db_pass = os.getenv('POSTGRES_PASSWORD')
        db_host = 'db'
        db_name = os.getenv('POSTGRES_DB')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}'
    else:
        # Если передали test_config (например, из pytest) — загружаем его
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from .models import User
        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app