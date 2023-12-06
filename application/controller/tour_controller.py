from fileinput import filename

from flask import Blueprint, current_app
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from application.model.database import connect_to_db, close_connection
from application.model.dbbooking import find_all_usernames_for_tour, \
    mark_all_bookings_from_specific_tour_as_inactive_in_db, mark_all_bookings_from_specific_tour_as_inactive_in_list
from application.model.dbtour import insert_tour_to_db, get_rows_tours, mark_tour_as_inactive_in_db
from application.model.dbtour import update_plasser_ledig
from application.model.tour import Tour, list_of_tours
from application.model.tour import add_tourgoers_to_list_of_created_tours, \
    add_spots_available_to_list_of_created_tours, mark_tour_as_inactive_in_list_of_tours
from application.model.user import get_tour_ids_from_tours_from_specific_user, get_tours_from_specific_user

tour_blueprint = Blueprint("tour", __name__)

@tour_blueprint.route("/tours")
def tours():
    return render_template("tours.html")


@tour_blueprint.route("/logged_in_tours", methods=("GET", "POST"))
@login_required
def logged_in_tours():
    return render_template("logged_in_tours.html")


@tour_blueprint.route("/my_tours", methods=("GET", "POST"))
@login_required
def my_tours():
    user = current_user
    conn, cur = connect_to_db(current_app)
    list_of_created_tours = get_tours_from_specific_user(cur, user.id)
    current_users_tour_ids = get_tour_ids_from_tours_from_specific_user(list_of_created_tours)
    tour_id_with_usernames = find_all_usernames_for_tour(cur, current_users_tour_ids)
    list_of_created_tours = add_tourgoers_to_list_of_created_tours(tour_id_with_usernames, list_of_created_tours)
    update_plasser_ledig(cur)
    conn.close()
    list_of_created_tours = add_spots_available_to_list_of_created_tours(list_of_created_tours)
    return render_template("my_tours.html",
                           list_of_created_tours=list_of_created_tours)


@tour_blueprint.route("/create_tour", methods=("GET", "POST"))
@login_required
def create_tour():
    # https://www.youtube.com/watch?v=I9BBGulrOmo -->image input
    if request.method == "POST":
        # Henter inn data fra input of lagrer i variabler
        title = request.form["title"]
        max_capacity = request.form["max_capacity"]
        description = request.form["description"]
        location = request.form["location"]
        date = request.form["date"]
        price = request.form["price"]

        if not title:
            flash("Vennligst skriv inn tittel!")
        elif not max_capacity:
            flash("Vennligst skriv inn kapasitet!")
        elif not description:
            flash("Vennligst skriv inn beskrivelse!")
        elif not location:
            flash("Vennligst skriv inn lokasjon!")
        elif not date:
            flash("Vennligst skriv inn dato!")
        elif not price:
            flash("Vennligst skriv inn prisen!")

        else:
            user = current_user
            created_by = user.id

            conn, cur = connect_to_db(current_app)
            insert_tour_to_db(conn, cur, title, int(max_capacity), description, location, date, int(price), created_by,
                              is_active=True)

            tour_id = get_rows_tours(cur)
            tour = Tour(tour_id, title, date, int(price), int(max_capacity), created_by, description, location,
                        is_active=True)
            tour.add_tour_to_list_of_tours(cur)  # flyttet fra tour inn hit for å kunne kjøre tester mot tour
            close_connection(conn)

            user.add_tour_to_list(tour)

            return redirect(url_for('tour.my_tours'))

    return render_template("create_tour.html")


@tour_blueprint.route("/notloggedtour/<int:tour_id>", methods=['GET'])
def outtour(tour_id, list_of_tours=list_of_tours):
    # Get info from the correct tour
    correct_tour = {}
    for single_tour in list_of_tours:
        if single_tour["id"] == tour_id:
            correct_tour.update(single_tour)

    return render_template("single_tour_not_logged_in.html", correct_tour=correct_tour)


@tour_blueprint.route("/loggedtour/<int:tour_id>", methods=['GET'])
@login_required
def intour(tour_id, list_of_tours=list_of_tours):
    correct_tour = {}
    for single_tour in list_of_tours:
        if single_tour["id"] == tour_id:
            correct_tour.update(single_tour)

    return render_template("tour.html", correct_tour=correct_tour)


@tour_blueprint.route("/cancel_tour", methods=["POST"])
@login_required
def cancel_tour():  # Basically copy-paste fra cancel_booking i booking_controller.py
    if request.method == "POST":
        # Denne koden setter is_active fra true to false når du trykker på "Kanseller bestilling" i my_tours
        tour_id = request.form.get("id_tour")
        conn, cur = connect_to_db(current_app)
        mark_tour_as_inactive_in_db(cur, conn, tour_id)
        mark_all_bookings_from_specific_tour_as_inactive_in_db(cur, conn, tour_id)
        conn.close()
        mark_tour_as_inactive_in_list_of_tours(tour_id)
        mark_all_bookings_from_specific_tour_as_inactive_in_list(tour_id)

        return redirect(url_for("tour.my_tours"))
    else:
        return "Det har oppstått en feil ved kansellering av tour"
