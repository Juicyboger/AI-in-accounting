import os
from app import app, db

# 获取数据库 URL
db_url = os.environ.get("DATABASE_URL")
# 如果使用了旧的 "postgres://" 前缀，则替换为 "postgresql://"
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5432))
    app.run(host='0.0.0.0', port=port)
