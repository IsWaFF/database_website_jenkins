from app.models import User, Invite, Achievement

def test_registration_logic(client, app):
    with app.app_context():
        # 1. Создаем инвайт в тестовой базе
        inv = Invite(code="TEST_CODE")
        db.session.add(inv)
        db.session.commit()

    # 2. Пытаемся зарегистрироваться
    response = client.post('/register', data={
        'login': 'tester',
        'password': 'password123',
        'invite_code': 'TEST_CODE'
    }, follow_redirects=True)

    assert response.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(login='tester').first()
        assert user is not None
        # Проверяем ачивку Beta User
        assert any(a.name == 'Beta User' for a in user.achievements)
        # Проверяем, что инвайт "погашен"
        inv_used = Invite.query.filter_by(code="TEST_CODE").first()
        assert inv_used.is_used == True

def test_invalid_invite(client):
    response = client.post('/register', data={
        'login': 'hacker',
        'password': '123',
        'invite_code': 'WRONG_CODE'
    }, follow_redirects=True)
    
    assert "Неверный или использованный инвайт код!" in response.data.decode('utf-8')