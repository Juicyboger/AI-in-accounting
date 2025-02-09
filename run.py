import os
from app import app, db

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # 从环境变量中获取端口号，若不存在则默认使用 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

