from . import db
from flask_login import UserMixin
from datetime import datetime


# User database and snowboard info
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))

    skier_or_snowboarder = db.Column(db.String(50))
    skill_level = db.Column(db.String(50))
    bio = db.Column(db.String(1000))
    facebook_profile = db.Column(db.String(200))

    posts = db.relationship('Posts', backref='author', lazy=True)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


