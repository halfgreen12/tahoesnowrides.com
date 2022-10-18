from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import secrets
import string

db = SQLAlchemy()


# DB_NAME = "database.db"


# function to initialize Flask and MySQL database
def create_app():
    app = Flask(__name__)

    app.secret_key = ''.join(
        (secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(15)))

    # connect database
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Warriorswinin6!@localhost/user_info"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .auth import auth
    from .views import views

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app

# code to be used to create a new database
# def create_database(app):
#     with app.app_context():
#         db.create_all()
#     # if not path.exists('website/' + DB_NAME):
#     #     db.create_all(app=app)
#         print('Created Database!')
