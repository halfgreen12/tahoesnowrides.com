from . import db
from flask_login import UserMixin


# User database and snowboard info
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))

    stance = db.Column(db.String(50))
    board_size = db.Column(db.String(50))
    boot_size = db.Column(db.String(50))
    # add more columns for snowboard info


# maybe add database for photos

