import flask_login

""" Her er tanken at når man lager en bruker så må de skrive inn brukernavn, passord og email,
men resten av infoen er frivillig de kan putte inn senere"""
list_of_all_users = []


def length_of_all_user_list():
    # Denne funksjonen er bare for å få ut antall brukere i systemet
    return len(list_of_all_users)


def get_tour_ids_from_tours_from_specific_user(tour_from_specific_user):
    tour_id_list = []
    for tour in tour_from_specific_user:
        tour_id_list.append(tour["id"])
    return tour_id_list


def get_tours_from_specific_user(cur, user_id):
    liste = []
    sql = "SELECT * FROM tours WHERE created_by = (?) AND is_active = True"
    cur.execute(sql, (user_id,))
    info_retrieved = cur.fetchall()
    if info_retrieved:
        for tuple in info_retrieved:
            temp_dict = {
                "id": tuple[0],
                "title": tuple[1],
                "max_capacity": tuple[2],
                "description": tuple[3],
                "location": tuple[4],
                "date": tuple[5],
                "price": tuple[6],
            }
            liste.append(temp_dict)

    return liste


class User(flask_login.UserMixin):
    def __init__(
            self,
            id,
            username,
            password,
            email,
            description=None,
            birthdate=None,
            gender=None,
            picture=None,
    ):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.list_of_bookings = []
        self.list_of_created_tours = []
        self.description = description
        self.birthdate = birthdate
        self.gender = gender
        self.picture = picture
        # Kanskje fjerne denne?
        list_of_all_users.append(username)

    # Testet
    def add_tour_to_list(self, tour):
        self.list_of_created_tours.append(tour)

    # Testet
    def get_list_of_created_tours(self):
        return self.list_of_created_tours

    # Testet
    def get_id(self):
        return str(self.id)

    def check_username_in_list(self, username):
        # En annen metode for å sjekke "databasen" om brukernavnet er unikt
        for x in list_of_all_users:
            if x == username:
                return True
        return False

    # Testet
    def add_info(self, description, birthdate, gender, picture=None):
        # Metode for å legge til mer info til en brukerprofil etter at objektet er instansiert
        self.description = description
        self.birthdate = birthdate
        self.gender = gender
        self.picture = picture

    # Testet
    def update_user_info(self, conn, cur, username, email, description, birthdate, gender):
        # Metode for å oppdatere infoen på brukerprofilen
        if username != "":
            self.username = username
            self.update_user_value_in_db(conn, cur, "username", username)

        if email != "":
            self.email = email
            self.update_user_value_in_db(conn, cur, "email", email)

        if description != "":
            self.description = description
            self.update_user_value_in_db(conn, cur, "description", description)

        if birthdate != "":
            self.birthdate = birthdate
            self.update_user_value_in_db(conn, cur, "birthdate", birthdate)

        if gender != "":
            self.gender = gender
            self.update_user_value_in_db(conn, cur, "gender", gender)

    """Kan eventuelt slå sammen de to over, får se an senere

    # Denne må vel flyttes til booking eller slettes
    def book_tour(self, tour, joining_participants):
        print(f"tour før: {tour}")
        # todo: fikse dette - må lage ny table i database først
        # nå er det (basically) bare printing som skjer
        tour['max_capacity'] = int(tour['max_capacity']) - joining_participants
        print(f"tour etter: {tour}")
        
        self.list_of_bookings.append(tour)
        print("Successfully booked tour")

    """

    # Testet
    def change_password(self, conn, cur, new_password):
        # Endrer passord i database
        self.update_user_value_in_db(conn, cur, "password", new_password)
        # Endrer passord på user objektet
        self.password = new_password

    # Testet
    def update_user_value_in_db(self, conn, cur, key, new_value):
        # key - hvilken kolonne du vil forandre. Må være string.
        # new_value - hva du vil verdien skal være

        # Må omforme key til å bli "key" slik at det fungerer med sql-spørringen
        fixed_key = f'"{key}"'

        try:
            update_pass = f"UPDATE users SET {fixed_key} = ? WHERE id = ?"
            variables = (new_value, self.get_id())
            cur.execute(update_pass, variables)
            conn.commit()
        except Exception as e:
            print(
                f"Error updating '{key}' to the new value of '{new_value}' using update_user_value_in_db()"
                f" in user.py: {str(e)}"
            )

    # Testet

