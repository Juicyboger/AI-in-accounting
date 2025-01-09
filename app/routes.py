from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User
from app.chatbot import chatbot_response

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
        # 登录逻辑
        pass
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        user_input = request.json['message']
        response = chatbot_response(user_input)
        return jsonify({'response': response})
    return render_template('chat.html')
