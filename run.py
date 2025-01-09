from app import app
from app import db

if __name__ == '__main__':
    app.run(debug=True)

# 自动创建数据库
@app.before_first_request
def create_tables():
    db.create_all()