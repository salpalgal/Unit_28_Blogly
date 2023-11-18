
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    
    def __repr__(self):
        user =self
        return f"<User {user.id} {user.first_name} {user.last_name} {user.image_url}>"


    id = db.Column(db.Integer, primary_key =True, autoincrement = True)
    first_name = db.Column(db.String(30), nullable =False)
    last_name = db.Column(db.String(30), nullable =False)
    image_url = db.Column(db.String, nullable =False)
