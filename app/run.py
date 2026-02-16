from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Создаем таблицы если их нет
        db.create_all()
        
        # Создаем ПЕРВЫЙ инвайт, если база пустая, чтобы ты мог зарегаться
        from app.models import Invite
        if not Invite.query.first():
            print("База пуста! Создаю мастер-инвайт: DEV_GOD")
            master_invite = Invite(code='DEV_GOD')
            db.session.add(master_invite)
            db.session.commit()
            
    app.run(host='0.0.0.0', port=5000, debug=True)