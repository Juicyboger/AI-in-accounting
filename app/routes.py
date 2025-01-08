from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from run import app, db
from app.models import User
from app.chatbot import chatbot_response

@app.route('/')
def home():
    return render_template('home.html')

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
