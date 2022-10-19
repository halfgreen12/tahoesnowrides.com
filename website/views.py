from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request

from website import weather_api


views = Blueprint('views', __name__)


ride_posts = [
    {
        'author': 'Neil Griffin',
        'title': 'Ride to Heavenly',
        'content': "Hey I'm offering a ride to heavenly this Saturday. I've got dogs in the car though. Split gas.",
        'date_posted': 'October, 15th 2022'
    },
    {
        'author': 'Shaun White',
        'title': 'Ride to North Lake ',
        'content': "Hey I'm offering a ride to northstar this Sunday! Leaving at 5:30am from the East Bay.",
        'date_posted': 'October, 18th 2022'
    }
]


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
    return render_template("posts.html", user=current_user, ride_posts=ride_posts)
