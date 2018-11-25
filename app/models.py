from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    comments = db.relationship('Comment',backref = 'comments',lazy = "dynamic")

    @property  
    def password(self): 
        raise AttributeError('You cannot read the password attribute') 


    @password.setter 
    def password(self, password):   
        self.pass_secure = generate_password_hash(password)   

    def verify_password(self,password):   
        return check_password_hash(self.pass_secure,password)


    def __repr__(self):
        return f'User {self.username}'




class Blog(UserMixin,db.Model):

    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255))
    heading = db.Column(db.String(255))
    blog = db.Column(db.String(1000))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
   
    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()        


class Comment(UserMixin,db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255))
    comment = db.Column(db.String(10000))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    
   
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()        


    def delete_comment(self, comment):
        db.session.delete(comment)
        db.session.commit()