from app import db

class User(db.Model):
    # 你的字段定义，例如 id, username, password 等
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    @property
    def is_authenticated(self):
        return True