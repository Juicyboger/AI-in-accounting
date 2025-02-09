from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # 存储经过哈希加密后的密码
    password_hash = db.Column(db.String(128), nullable=False)
    # 管理员标识，默认非管理员
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """使用 Werkzeug 的函数生成密码哈希"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码是否正确"""
        return check_password_hash(self.password_hash, password)

    # 以下属性和方法可用于 Flask-Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)


class ChatbotFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 外键关联到 User 表，确保每条反馈都有对应的用户
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answer = db.Column(db.Text, nullable=False)   # 聊天机器人生成的答案
    rating = db.Column(db.Integer, nullable=False)  # 评分，例如 1~5 星
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
