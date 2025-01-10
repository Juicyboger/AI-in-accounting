from flask import render_template, request, redirect, url_for, flash, session, g, jsonify
from . import app, db
from .models import User
from .chatbot import chatbot_response

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Please choose another."

        # 创建新用户
        new_user = User(username=username, password=password)  # 密码存储时建议加密
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))  # 注册成功后跳转到登录页面

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 检查用户名和密码
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id  # 使用 session 存储用户 ID
            session['username'] = user.username
            return redirect(url_for('chat'))  # 登录成功后跳转到聊天页面
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        user_input = request.json['message']
        response = chatbot_response(user_input)
        return jsonify({'response': response})
    return render_template('chat.html', username=session.get('username'))

@app.route('/logout')
def logout():
    session.clear()  # 清除会话
    return redirect(url_for('login'))  # 跳转到登录页面

@app.before_request
def load_current_user():
    """
    在每次请求之前检查用户是否已登录。
    如果 session 中有用户 ID，将用户信息加载到全局变量 g。
    """
    user_id = session.get('user_id')
    g.current_user = User.query.get(user_id) if user_id else None

@app.context_processor
def inject_user():
    """
    将当前用户注入到模板上下文中，使模板可以访问 current_user。
    """
    return {'current_user': g.current_user or None}

