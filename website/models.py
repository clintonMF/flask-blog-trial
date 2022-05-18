from tkinter import CASCADE
from sqlalchemy import ForeignKey
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 



class User(db.Model, UserMixin):
    """creating the database models"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    post = db.relationship('Post',backref='user',passive_deletes=True)
    comment = db.relationship('Comment',backref='user',passive_deletes=True)
    like = db.relationship('Like',backref='user',passive_deletes=True)
    # backref serves as a means of accessing the User table from the Post table
    # e.g Post.user would give everything in the User table
    # passive_deletes=True prevents sqlalchemy from null ing out the foreign keys
    
class Post(db.Model):
    """creating a database table  for the post"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    author = db.Column(db.Integer, ForeignKey('user.id', 
                       ondelete="CASCADE"), nullable=False)
    comment = db.relationship('Comment',backref='post',passive_deletes=True)
    like = db.relationship('Like',backref='post',passive_deletes=True)
    #  ondelete = cascade : this allows all post made by a user to be deleted if the user deletes his account.
    # this is to ensure there are no post without users after an account is deleted.
    
class Comment(db.Model):
    """Creating a databae table for the comments"""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    author = db.Column(db.Integer, ForeignKey('user.id', 
                       ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, ForeignKey('post.id', 
                       ondelete="CASCADE"), nullable=False)
    
class Like(db.Model):
    """Creating a database table for the likes"""
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    author = db.Column(db.Integer, ForeignKey('user.id', 
                       ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, ForeignKey('post.id', 
                       ondelete="CASCADE"), nullable=False)
    
