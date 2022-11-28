from .models import User

from flask import Blueprint, render_template, request, redirect, url_for
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


@views.route('/user/<user_clicked_on>', methods=['GET'])
@login_required
def user_profile(user_clicked_on):
    user_clicked_on = User.query.filter_by(id=user_clicked_on).first_or_404()
    if user_clicked_on.id == current_user.id:
        return redirect(url_for('views.home'))
    return render_template("user_profile.html", user=current_user, user_clicked_on=user_clicked_on)
