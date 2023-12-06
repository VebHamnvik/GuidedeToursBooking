from flask import Blueprint, current_app
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application.model.database import connect_to_db
from application.model.dbtour import update_plasser_ledig
from application.model.tour import list_of_tours

home_blueprint = Blueprint("home", __name__)

@home_blueprint.route("/")
def home():
    conn, cur = connect_to_db(current_app)
    update_plasser_ledig(cur)
    conn.close()

    return render_template("index.html", list_of_tours=list_of_tours)

@home_blueprint.route("/dashboard", methods=("GET", "POST"))
@login_required
def dashboard():
    if current_user.is_authenticated:
        conn, cur = connect_to_db(current_app)
        update_plasser_ledig(cur)
        conn.close()

        return render_template("dashboard.html", list_of_tours=list_of_tours)
    else:
        return "Not logged in"
