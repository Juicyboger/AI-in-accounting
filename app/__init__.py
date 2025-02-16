from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 初始化 Flask 应用
app = Flask(__name__)

# 配置 Flask 应用
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please configure it in your .env file or environment variables.")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 设置 SECRET_KEY
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# 初始化数据库和登录管理
db = SQLAlchemy(app)

# 导入路由（注意：放在初始化之后）
from app import routes