# admin.py
from app import app, db
from app.models import User, ChatbotFeedback

with app.app_context():
    # 1. 检查是否存在管理员账号（以用户名 'admin' 为例）
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password='admin123', is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print("管理员账号已创建：用户名：admin, 密码：admin123")
    else:
        print("管理员账号已存在")

    # 2. 查询所有用户反馈记录，并按时间倒序输出
    feedbacks = ChatbotFeedback.query.order_by(ChatbotFeedback.timestamp.desc()).all()
    if feedbacks:
        print("\n用户反馈报告：")
        for fb in feedbacks:
            print(f"ID: {fb.id}, 用户ID: {fb.user_id}, 答案: {fb.answer}, 评分: {fb.rating}, 时间: {fb.timestamp}")
    else:
        print("\n当前没有用户反馈记录。")
