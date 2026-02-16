import pytest
from app import create_app, db
from app.models import Invite, Achievement

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", # База в памяти
    })

    with app.app_context():
        db.create_all()
        # Создаем базовые данные для тестов
        a = Achievement(name='Beta User', description='Test')
        db.session.add(a)
        db.session.commit()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()