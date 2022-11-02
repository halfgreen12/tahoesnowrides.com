from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import secrets
import string
import os

db = SQLAlchemy()
mail = Mail()

db_connection = os.environ.get('NEW_FLASK_SNOWBOARD_DB_CONNECTION')
email_password = os.environ.get('NEW_FLASK_SNOWBOARD_EMAIL_PASSWORD')


# function to initialize Flask and MySQL database
def create_app():
    app = Flask(__name__)

    app.secret_key = ''.join(
        (secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(15)))

    # connect database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # configuration for send password reset email
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = '587'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'snow.rides530@gmail.com'
    app.config['MAIL_PASSWORD'] = email_password
    mail.init_app(app)

    from .auth import auth
    from .views import views
    from .ride_posts import ride_posts_blueprint
    from .error_handlers import errors
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(ride_posts_blueprint, url_prefix='/')
    app.register_blueprint(errors, url_prefix='/')

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
