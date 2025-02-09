from app import app, db

with app.app_context():
    db.create_all()

from app import db
from app.models import User

# 创建管理员账号，用户名为 admin，密码为 admin123（请根据需要更改）
admin = User(username='admin', password='admin123', is_admin=True)
db.session.add(admin)
db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5432)