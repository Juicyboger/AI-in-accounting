from app import app, db

with app.app_context():
    db.drop_all() 
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)