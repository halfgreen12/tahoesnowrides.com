from .models import Posts, User
from . import db

from flask import Blueprint, render_template, flash, request, redirect, url_for, abort
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
    skier_or_snowboarder = current_user.skier_or_snowboarder
    skill_level = current_user.skill_level
    bio = current_user.bio

    # weather api call from user input
    if request.method == "POST":
        city = request.form['city']
        [result1, result2] = weather_api.main(city)

    return render_template("home.html", user=current_user, full_name=full_name,
                           skier_or_snowboarder=skier_or_snowboarder, skill_level=skill_level,
                           bio=bio, result1=result1, result2=result2)


@views.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    page = request.args.get('page', 1, type=int)
    ride_posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("posts.html", user=current_user, ride_posts=ride_posts)


@views.route('/posts/new', methods=['GET', 'POST'])
@login_required
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


@views.route('/single_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def single_post(post_id):
    ride_post = Posts.query.get_or_404(post_id)
    return render_template("single_post.html", user=current_user, ride_post=ride_post)


@views.route('/single_post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    ride_post_to_delete = Posts.query.get_or_404(post_id)
    if ride_post_to_delete.author != current_user:
        abort(403)
    db.session.delete(ride_post_to_delete)
    db.session.commit()
    flash('Your post has been deleted!', 'success')

    return redirect(url_for('views.posts'))


@views.route('/user/<user_clicked_on>', methods=['GET'])
@login_required
def user_profile(user_clicked_on):
    user_clicked_on = User.query.filter_by(id=user_clicked_on).first_or_404()
    if user_clicked_on.id == current_user.id:
        return redirect(url_for('views.home'))
    return render_template("user_profile.html", user=current_user, user_clicked_on=user_clicked_on)
