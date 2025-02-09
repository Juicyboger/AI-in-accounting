from app import app, db
from app.models import User

with app.app_context():
    # 检查是否存在管理员账号（以用户名 'admin' 为例）
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password='admin123', is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("管理员账号已创建：用户名：admin, 密码：admin123")
    else:
        print("管理员账号已存在")