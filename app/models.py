from app import db

class User(db.Model):
    # 你的字段定义，例如 id, username, password 等
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # 新增字段，默认False

    @property
    def is_authenticated(self):
        return True

# models.py
from datetime import datetime

class ChatbotFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)  # 聊天机器人生成的答案
    rating = db.Column(db.Integer, nullable=False)  # 例如 1~5 星
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_authenticated(self):
        return True