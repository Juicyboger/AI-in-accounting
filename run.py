import os
from app import app, db
from app.models import User

with app.app_context():
    # 创建所有数据表（如果还不存在）
    db.create_all()
    
    # 自动检查并创建管理员账号
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password='admin123', is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("管理员账号已创建：用户名：admin, 密码：admin123")
    else:
        print("管理员账号已存在")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
