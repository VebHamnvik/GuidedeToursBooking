from application.model.dbbooking import get_users_from_bookings
import base64

from application.model.database import connect_to_db
from application.model.dbuser import get_username_by_id
from application.model.tour import list_of_tours, Tour


def get_rows_tours(cur):
    sql3 = '''SELECT COUNT(id) FROM tours'''
    cur.execute(sql3)
    result = cur.fetchone()
    tour_id = result[0]

    return tour_id


def insert_tour_to_db(conn, cur,
                      title, max_capacity, description, location, date, price, created_by, is_active=True):
    sql = """ INSERT INTO tours(title,max_capacity, description, location, date, price, created_by, is_active)
                                                                  VALUES(?,?,?, ?, ?, ?, ?, ?) """
    sql_tour = (title, max_capacity, description, location, date, price, created_by, is_active)
    # Legges inn i databasen med brukernavn, passord, email. ID blir automatisk opprettet
    cur.execute(sql, sql_tour)
    conn.commit()


def update_tour_is_active(conn, cur, tour_id, is_active=0):
    try:
        cur.execute("UPDATE tours SET is_active = ? WHERE id = ?", (is_active, tour_id))
        print({tour_id})
        conn.commit()
    except Exception as e:
        print(f"Error while updating is_active for the tour: {str(e)}")
        conn.rollback()


# skrevet ny som gjør is active = False, men har ikke slettet tidligere delete_tour_by_id, trengs denne nå?
def delete_tour_by_id(conn, cur, tour_id):
    try:
        update_tour_is_active(conn, cur, tour_id, is_active=False)
    except Exception as e:
        print(f'Feil under sletting av tur: {str(e)}')


def add_tour_to_list_from_db(cur):
    sql = "SELECT * FROM tours where is_active = True"
    cur.execute(sql)
    info_retrieved = cur.fetchall()

    # tuple[0] = id
    # tuple[1] = title
    # tuple[2] = max_capacity
    # tuple[3] = beskrivelse
    for tuple in info_retrieved:
        # Henter ut en liste med user_id som har en booking registrert på denne tour_id-en
        tour_id = int(tuple[0])
        list_of_users_who_booked_tour = get_users_from_bookings(cur, tour_id)
        list_of_usernames = []

        for user in list_of_users_who_booked_tour:
            # Går gjennom listen med user_id's og henter ut usernames
            username = get_username_by_id(cur, user)
            if username not in list_of_usernames:
                list_of_usernames.append(username)

        temp_dict = {
            "id": tuple[0],
            "title": tuple[1],
            "max_capacity": tuple[2],
            "description": tuple[3],
            "location": tuple[4],
            "date": tuple[5],
            "price": tuple[6],
            "created_by": tuple[7],
            "is_active": tuple[8],
            # Lager en ny key:value med en liste med usernames som har booket touren
            "booked_by": list_of_usernames

        }
        list_of_tours.append(temp_dict)
    return list_of_tours


def get_tour_by_id(cur, tour_id):
    sql = '''SELECT * FROM tours WHERE id = ?'''
    cur.execute(sql, (tour_id,))
    tour_object = cur.fetchone()

    if tour_object:
        id, title, max_capacity, description, location, date, price, created_by, is_active, image = tour_object
        tour = Tour(id, title, date, price, max_capacity, created_by, description, location, is_active)
        return tour
    return None


def update_plasser_ledig(cur):
    # Henter totalen av participants for alle aktive bookinger
    sql = '''SELECT id_tour, participants FROM booking WHERE is_active = True'''
    cur.execute(sql)
    sql_results = cur.fetchall()

    # Kobler opp alle participants med en tour_id i en dictionary
    participants_dict = {}
    for tour_id, participants in sql_results:
        if tour_id in participants_dict:
            participants_dict[tour_id] += participants
        else:
            participants_dict[tour_id] = participants

    # Finner hvor mange plasser som er ledige for hver tour og legger dette til i list_of_tours
    for tour in list_of_tours:
        if str(tour['id']) in participants_dict:
            tour['spots_available'] = int(tour['max_capacity']) - int(participants_dict[str(tour['id'])])

    # Legger til spots_available for alle tours som ikke har fått det av forrige løkke
    for tour in list_of_tours:
        if 'spots_available' not in tour:
            tour['spots_available'] = tour['max_capacity']


def mark_tour_as_inactive_in_db(cur, conn, tour_id):
    sql = f'''UPDATE tours SET is_active = False WHERE id = {tour_id}'''
    cur.execute(sql)
    conn.commit()

