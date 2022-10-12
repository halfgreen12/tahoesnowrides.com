from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request

from website import weather_api


views = Blueprint('views', __name__)


@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    result = ""
    full_name = current_user.full_name
    stance = current_user.stance
    boot_size = current_user.boot_size
    board_size = current_user.board_size
    if request.method == "POST":
        city = request.form['city']
        result = weather_api.main(city)

    return render_template("home.html", user=current_user, full_name=full_name,
                           stance=stance, boot_size=boot_size,
                           board_size=board_size, result=result)
