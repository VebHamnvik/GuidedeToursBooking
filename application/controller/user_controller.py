from flask import Blueprint, current_app
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from application.model.database import connect_to_db, close_connection
from application.model.dbuser import get_username_from_db, insert_user_info_to_db, get_password_from_db, \
    get_id_by_username, get_user_by_id
from application.model.helpfunctions import check_two_passwords, validate_username, validate_password
from application.model.user import list_of_all_users

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/registrer", methods=("GET", "POST"))
def registrer_user():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        email = request.form["email"]

        if not username:
            flash("Brukernavn kreves!")
        elif not validate_username(username):
            flash("Vennligst skriv ett brukernavn som er lengre enn 3 tegn")
        elif not password:
            flash("Passord kreves!")
        elif not validate_password(password):
            flash("Vennligst skriv et passord som er lengre enn 4 tegn")
        elif not password2:
            flash("Passord kreves!")
        elif not validate_password(password):
            flash("Vennligst skriv et passord som er lengre enn 4 tegn")
        elif not email:
            flash("Email kreves!")
        elif check_two_passwords(password, password2) == False:
            flash("Passordene matcher ikke!")
        else:
            # list_of_all_users kan nok fjernes nå som databasen fungerer
            list_of_all_users.append({"brukernavn": username, "email": email})
            # Lagrer inputene i variabel slik at den kan sendes inn til databasen senere
            conn, cur = connect_to_db(current_app)
            username_check = get_username_from_db(cur, username)
            close_connection(conn)
            # Hvis det ikke finnes i databasen
            if username_check is None:
                conn, cur = connect_to_db(current_app)
                insert_user_info_to_db(conn, cur, username, password, email)
                close_connection(conn)
                return redirect(url_for("user.login"))
            else:
                flash("Brukernavnet er allerede i bruk")

    return render_template("registrer.html")

@user_blueprint.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username:
            flash("Brukernavn kreves!")

        elif not password:
            flash("Passord kreves!")

        else:
            conn, cur = connect_to_db(current_app)
            username_db = get_username_from_db(cur, username)
            password_db = get_password_from_db(cur, username)

            # Sjekker at brukeren finnes i databasen
            if username_db is not None:
                # Lagrer id-en i en variabel som blir hentet ut fra en funksjon der brukernavnet er sendt inn som
                # argument
                user_id = get_id_by_username(cur, username_db[0])
                # Bruker denne id-en til å hente ut all info i databasen om denne personen og lager et objekt
                user_info = get_user_by_id(cur, user_id)

                # Sjekker om pass_row eksisterer
                if password_db is not None:
                    # Sjekker passord skrevet inn mot passord i databasen
                    if check_two_passwords(password_db[0], password):
                        # Sender inn det userobjektet som ble opprettet tidligere med get_user_by_id
                        login_user(user_info)
                        # Bruker blir logget inn og videresendt til dashboard
                        return redirect(url_for("home.dashboard"))
                    else:
                        flash("Feil brukernavn eller passord")
                # Hvis passordet ikke stemmer
                else:
                    flash("Feil brukernavn eller passord")
            # Hvis brukernavnet ikke er i databasen
            else:
                flash("Feil brukernavn eller passord")
    return render_template("login.html")

@user_blueprint.route("/my_profile", methods=("GET", "POST"))
@login_required
def my_profile():
    user = current_user
    username = user.username
    email = user.email
    description = user.description
    birthdate = user.birthdate
    gender = user.gender

    return render_template("user_profile.html", username=username, email=email,
                           description=description, birthdate=birthdate, gender=gender)

@user_blueprint.route("/change_profile", methods=("GET", "POST"))
@login_required
def change_profile():
    if request.method == "POST":
        # Henter inn data fra input of lagrer i variabler
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]
        birthdate = request.form["birthdate"]
        gender = request.form["gender"]

        # Henter ut det innloggede brukerobjektet
        user = current_user

        # Kaller funksjon for å oppdatere bruker informasjon
        conn, cur = connect_to_db(current_app)
        user.update_user_info(conn, cur, username, email, description, birthdate, gender)
        close_connection(conn)
        flash("Informasjon oppdatert!")

    return render_template("change_profile.html")

@user_blueprint.route("/change_password", methods=("GET", "POST"))
@login_required
def change_password():
    if request.method == "POST":
        # Henter inn data fra input of lagrer i variabler
        old_password = request.form["old_password"]
        new_password1 = request.form["new_password1"]
        new_password2 = request.form["new_password2"]

        user = current_user
        old_password_check = user.password

        if not old_password:
            flash("Vennligst skriv inn det gamle passordet!")
        elif not new_password1:
            flash("Vennligst skriv inn det nye passordet!")
        elif not validate_password(new_password1):
            flash("Vennligst skriv inn ett passord som er lengre enn 4 tegn")
        elif not new_password2:
            flash("Vennligst gjenta det nye passordet!")
        elif not check_two_passwords(new_password1, new_password2):
            flash("Det nye passordet matcher ikke hverandre")
        elif not check_two_passwords(old_password_check, old_password):
            flash("Du har skrevet inn feil gammelt passord")
        else:
            conn, cur = connect_to_db(current_app)
            user.change_password(conn, cur, new_password2)
            flash("passord endret :)")

    return render_template("change_password.html")

@user_blueprint.route("/logout", methods=('GET', 'POST'))
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@user_blueprint.route("/user_profile/<int:user_id>")
def user_profile(user_id):
    return render_template("user.guide_info")