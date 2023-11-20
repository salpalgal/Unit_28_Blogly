
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from datetime import datetime
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

class Post(db.Model):
    __tablename__ = 'posts'
     
    def __repr__(self):
        post = self
        return f"<Post {post.id} {post.title} {post.content} {post.created_at} {post.user.id}>"

    id = db.Column(db.Integer, primary_key =True, autoincrement = True)
    title = db.Column(db.String(30), nullable = False)
    content = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime(), nullable= False, default = datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_post = db.relationship('User')