from flask import Blueprint, render_template, request, flash,  redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
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

