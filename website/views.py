from .models import Posts
from . import db

from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user

from website import weather_api


views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    result1 = ""
    result2 = ""

    # return user snowboard info
    full_name = current_user.full_name
    stance = current_user.stance
    boot_size = current_user.boot_size
    board_size = current_user.board_size

    # weather api call from user input
    if request.method == "POST":
        city = request.form['city']
        [result1, result2] = weather_api.main(city)

    return render_template("home.html", user=current_user, full_name=full_name,
                           stance=stance, boot_size=boot_size,
                           board_size=board_size, result1=result1, result2=result2)


@views.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    ride_posts = Posts.query.all()
    return render_template("posts.html", user=current_user, ride_posts=ride_posts)


@views.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        post = Posts(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('views.posts'))

    return render_template("create_post.html", user=current_user)
