from .models import Posts
from . import db

from flask import Blueprint, render_template, flash, request, redirect, url_for, abort
from flask_login import login_required, current_user


ride_posts_blueprint = Blueprint('ride_posts_blueprint', __name__)


@ride_posts_blueprint.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    page = request.args.get('page', 1, type=int)
    all_ride_posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("posts.html", user=current_user, all_ride_posts=all_ride_posts)


@ride_posts_blueprint.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        post = Posts(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('ride_posts_blueprint.posts'))
    return render_template("create_post.html", user=current_user)


@ride_posts_blueprint.route('/single_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def single_post(post_id):
    ride_post = Posts.query.get_or_404(post_id)
    return render_template("single_post.html", user=current_user, ride_post=ride_post)


@ride_posts_blueprint.route('/single_post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    ride_post_to_delete = Posts.query.get_or_404(post_id)
    if ride_post_to_delete.author != current_user:
        abort(403)
    db.session.delete(ride_post_to_delete)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('ride_posts_blueprint.posts'))


