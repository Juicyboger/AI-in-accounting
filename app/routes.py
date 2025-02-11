from flask import render_template, request, redirect, url_for, flash, session, g, jsonify, abort
from . import app, db
from .models import User, ChatbotFeedback
from .chatbot import chatbot_response
from .finance_data import fetch_sg_stock_price

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
            # 根据用户是否为管理员来决定跳转页面
            if getattr(user, 'is_admin', False):
                return redirect(url_for('home'))  # 管理员跳转到首页（home.html），首页中显示管理员专用链接
            else:
                return redirect(url_for('home'))  # 普通用户跳转到聊天页面
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

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    sg_symbols = ["D05.SI", "O39.SI", "U11.SI"]
    stock_prices = []

    for sym in sg_symbols:
        data = fetch_sg_stock_price(sym)
        if data:
            stock_prices.append(data)
        else:
            print(f"Failed to get yfinance data for {sym}")

    return render_template('dashboard.html', stock_prices=stock_prices)


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

@app.route('/transfer', methods=['GET'])
@login_required
def transfer_page():
    return render_template('transfer.html')

# routes.py
from flask import request, jsonify, g
from .models import ChatbotFeedback

@app.route('/feedback', methods=['POST'])
@login_required
def feedback():
    data = request.get_json()
    rating = data.get('rating')
    answer = data.get('answer')
    
    if rating is None or answer is None:
        return jsonify({'error': 'Rating and answer are required'}), 400

    # 检查当前用户是否已经对这条回答提交过反馈（假设回答文本作为唯一标识）
    existing = ChatbotFeedback.query.filter_by(user_id=g.current_user.id, answer=answer).first()
    if existing:
        return jsonify({'error': 'Feedback for this answer has already been submitted.'}), 400

    new_feedback = ChatbotFeedback(
        user_id=g.current_user.id,
        rating=rating,
        answer=answer
    )
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback recorded successfully'})

@app.route('/feedback_report')
def feedback_report():
    feedbacks = ChatbotFeedback.query.order_by(ChatbotFeedback.timestamp.desc()).all()
    return render_template('feedback_report.html', feedbacks=feedbacks)




