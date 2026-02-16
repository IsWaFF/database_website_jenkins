import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Загружаем секреты из папки secrets
load_dotenv(os.path.join(os.path.dirname(__file__), '../secrets/.env'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# Подключение к PostgreSQL
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_host = 'db' # Имя сервиса в docker-compose
db_name = os.getenv('POSTGRES_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "<h1>DevOps Social App is Running!</h1>"

if __name__ == '__main__':
    # Слушаем на 0.0.0.0 чтобы было видно извне контейнера
    app.run(host='0.0.0.0', port=5000, debug=True)