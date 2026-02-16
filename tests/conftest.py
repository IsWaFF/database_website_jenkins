import pytest
from app import create_app, db
from app.models import Achievement

@pytest.fixture
def app():
    # Создаем конфиг специально для тестов
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test_secret"
    }
    
    app = create_app(test_config)

    with app.app_context():
        db.create_all()
        # Создаем ачивку для тестов, если её нет
        if not Achievement.query.filter_by(name='Beta User').first():
            a = Achievement(name='Beta User', description='Test')
            db.session.add(a)
            db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()