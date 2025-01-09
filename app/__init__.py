from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 初始化 Flask 应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# 初始化数据库和登录管理
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 导入路由（注意：放在初始化之后）
from app import routes

