from flask import Blueprint, current_app
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from application.model.dbbooking import create_booking, update_list_of_bookings, \
    check_if_participants_exceed_max_capacity, mark_booking_as_inactive, add_plasser_ledig_to_correct_bookings, \
    update_booking, check_for_existing_booking, find_info_about_tours_user_has_booked
from application.model.database import connect_to_db, close_connection
from application.model.tour import list_of_tours

booking_blueprint = Blueprint("booking", __name__)


@booking_blueprint.route("/my_bookings", methods=("GET", "POST"))
@login_required
def my_bookings():
    conn, cur = connect_to_db(current_app)
    update_list_of_bookings(cur)
    correct_bookings = find_info_about_tours_user_has_booked(cur, current_user.id)
    correct_bookings = add_plasser_ledig_to_correct_bookings(cur, correct_bookings)
    conn.close()

    return render_template("my_bookings.html", correct_bookings=correct_bookings)


@booking_blueprint.route("/book_this_tour/<int:book_tour_id>", methods=('GET', 'POST'))
@login_required
def book_this_tour(book_tour_id, list_of_tours=list_of_tours):
    # Hvis man allerede har booket for si 2 stk, og trykker på registrer igjen med 3 stk
    # legger create_or_update_booking_in_db() bare til 2 + 3 = 5 slik at man har registrert 5 stk
    # for den touren.
    # todo 1: gjør at denne siden spør "er du sikker på at du vil legge til X fler? (du har allerede booket for Y)
    # todo 4: gjør at en bruker kan trekke fra antall participants ( vi var 3 som skulle dra, men 1 gadd ikke!!)

    if request.method == "POST":
        # Henter antall som skal på tur
        people_going = int(request.form['participants'])
        if people_going < 1:
            flash("Du kan ikke booke for mindre enn 1 person :/")
            flash("Prøv igjen.")
        else:
            correct_tour = {}
            # finner riktig tour :)
            for single_tour in list_of_tours:
                if single_tour["id"] == book_tour_id:
                    correct_tour.update(single_tour)

            # check if booking exists
            conn, cur = connect_to_db(current_app)
            does_it_exist = check_for_existing_booking(cur, current_user.id, correct_tour['id'])

            # Checks if this order will exceed max capacity
            if not check_if_participants_exceed_max_capacity(cur, correct_tour['id'], people_going):
                # If booking already exists - update it
                if does_it_exist:
                    update_booking(conn, cur, current_user.id, correct_tour['id'], people_going)
                    close_connection(conn)
                    return redirect(url_for("booking.fake_payment"))
                else:
                    create_booking(conn, cur, current_user.id, correct_tour['id'], people_going)
                    close_connection(conn)
                    return redirect(url_for("booking.fake_payment"))
            else:
                flash("Beklager, det er ikke plass til så mange mennesker på denne turen.")

    return render_template("book_this_tour.html", book_tour_id=book_tour_id)


@booking_blueprint.route("/fake_payment")
@login_required
def fake_payment():
    return render_template("fake_payment.html")


@booking_blueprint.route("/cancel_booking", methods=["POST"])
@login_required
def cancel_booking():
    if request.method == "POST":
        # Denne koden setter is_active fra true to false når du trykker på "Kanseller bestilling" i my_bookings
        tour_id = request.form.get("id_tour")
        user_id = request.form.get("id_user")
        conn, cur = connect_to_db(current_app)
        mark_booking_as_inactive(cur, conn, user_id, tour_id)
        conn.close()

        return redirect(url_for("booking.my_bookings"))
    else:
        return "Det har oppstått en feil ved kansellering av tour"
