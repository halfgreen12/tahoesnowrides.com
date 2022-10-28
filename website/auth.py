from flask import Blueprint, render_template, request, flash,  redirect, url_for, current_app
from .models import User
from . import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already associated with an account.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(full_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 4:
            flash('Password must be at least 4 characters.', category='error')
        else:
            new_user = User(email=email, full_name=full_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created.', category='success')
            return redirect(url_for('auth.info'))

    return render_template("sign_up.html", user=current_user)


# page for user to add their snowboard info after signing up
@auth.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    if request.method == 'POST':
        skier_or_snowboarder = request.form.get('skier_or_snowboarder')
        skill_level = request.form.get('skill_level')
        bio = request.form.get('bio')
        facebook_profile = request.form.get('facebook_profile')

        user_id = current_user.id
        user = User.query.filter_by(id=user_id).first()
        user.skier_or_snowboarder = skier_or_snowboarder
        user.skill_level = skill_level
        user.bio = bio.strip()
        user.facebook_profile = facebook_profile.strip()
        db.session.commit()
        flash("Profile complete.", category="success")
        return redirect(url_for('views.home'))
    return render_template("info.html", user=current_user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Snow Ride - Password Reset Request',
                  sender='snow.rides530@gmail.com',
                  recipients=[user.email],)
    msg.body = f"""To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}
    
If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)


# 1st page for resetting password (uses function defined in models.User class)
@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        check_for_user = User.query.filter_by(email=email).first()
        if check_for_user is None:
            flash('There is no account with that email. You must sign up first.')
        else:
            send_reset_email(check_for_user)
            flash('An email has been sent with instruction to reset your password.', category='info')
            return redirect(url_for('auth.login'))
    return render_template('reset_request.html', user=current_user)


# 2nd page for resetting password after clicking on email link (token)
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired link', category='error')
        return redirect(url_for('auth.reset_request'))
    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 4:
            flash('Password must be at least 4 characters.', category='error')
        else:
            hashed_password = generate_password_hash(password1, method='sha256')
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated! You are now able to log in.', category='success')
            return redirect(url_for('auth.login'))
    return render_template('reset_token.html', user=current_user)

