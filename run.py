import os
from app import app, db

if __name__ == '__main__':
    # 在主程序中创建应用上下文，并初始化数据库
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
