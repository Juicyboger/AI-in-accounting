from app import app, db
from app.models import User

with app.app_context():
    # 查询数据库中是否已经存在用户名为 "admin" 的账号
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        # 如果不存在，则创建一个管理员账号（用户名：admin，密码：admin123）
        admin = User(username='6666', password='6666', is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("管理员账号已创建：用户名：admin, 密码：admin123")
    else:
        print("管理员账号已存在")
