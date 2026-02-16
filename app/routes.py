from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User, Invite, Message, Achievement
import uuid
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import Invite, db

main = Blueprint('main', __name__)

# --- ГЛАВНАЯ И ЧАТ ---
@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        if current_user.is_banned:
            flash('Вы забанены и не можете писать.')
        else:
            msg_text = request.form.get('message')
            if msg_text:
                msg = Message(body=msg_text, author=current_user)
                db.session.add(msg)
                db.session.commit()
            return redirect(url_for('main.index'))
    
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return render_template('index.html', messages=messages)

# --- РЕГИСТРАЦИЯ (С инвайтами и Beta User) ---
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        invite_code = request.form.get('invite_code')

        # 1. Проверяем инвайт
        invite = Invite.query.filter_by(code=invite_code, is_used=False).first()
        if not invite:
            flash('Неверный или использованный инвайт код!')
            return redirect(url_for('main.register'))

        # 2. Проверяем логин
        user = User.query.filter_by(login=login).first()
        if user:
            flash('Логин занят!')
            return redirect(url_for('main.register'))

        # 3. Создаем юзера
        new_user = User(login=login, display_name=login, password=generate_password_hash(password))
        
        # ЛОГИКА BETA USER: Если юзер входит в первые 100
        user_count = User.query.count()
        if user_count < 100:
            beta_achieve = Achievement.query.filter_by(name='Beta User').first()
            # Если ачивки нет в базе, создадим её на лету (лучше это делать скриптом, но для теста сойдет)
            if not beta_achieve:
                beta_achieve = Achievement(name='Beta User', description='Один из первых 100!', image_name='beta.png')
                db.session.add(beta_achieve)
            new_user.achievements.append(beta_achieve)

        # 4. Гасим инвайт
        invite.is_used = True
        
        db.session.add(new_user)
        # Нужно сначала сохранить юзера, чтобы получить ID
        db.session.flush() 
        invite.used_by = new_user.id
        
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('main.index'))

    return render_template('register.html')

# --- ЛОГИН ---
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(login=login).first()

        if not user or not check_password_hash(user.password, password):
            flash('Неверный логин или пароль')
            return redirect(url_for('main.login'))

        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# --- ПРОФИЛЬ ---
@main.route('/user/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

@main.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    current_user.display_name = request.form.get('display_name')
    current_user.bio = request.form.get('bio')
    # Тут можно добавить загрузку авы
    db.session.commit()
    return redirect(url_for('main.profile', user_id=current_user.id))

@main.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.follow(user)
        db.session.commit()
    return redirect(url_for('main.profile', user_id=user_id))

# --- ЕДИНАЯ АДМИНКА ---
@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    # Проверка на админа
    if not current_user.is_admin:
        flash("Доступ запрещен!")
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        # 1. Логика генерации инвайта (из твоего админ.html)
        if 'generate_invite' in request.form:
            new_code = str(uuid.uuid4())[:8].upper()
            invite = Invite(code=new_code, created_by=current_user.id) # добавил создателя
            db.session.add(invite)
            db.session.commit()
            flash(f"Создан новый код: {new_code}")

        # 2. Логика банхаммера
        elif 'ban_user' in request.form:
            login_to_ban = request.form.get('login_to_ban')
            user_to_ban = User.query.filter_by(login=login_to_ban).first()
            if user_to_ban:
                user_to_ban.is_banned = True
                db.session.commit()
                flash(f"Пользователь {login_to_ban} успешно забанен!")
            else:
                flash("Пользователь не найден")

    # Получаем все инвайты для списка
    invites = Invite.query.all()
    return render_template('admin.html', invites=invites)