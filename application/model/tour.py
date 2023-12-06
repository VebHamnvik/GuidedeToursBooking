import string
import base64

list_of_tours = []


class Tour:
    def __init__(
        self,
        tour_id,
        title: string,
        date,
        price: float,
        max_capacity: int,
        created_by,
        description,
        location,
        is_active = True
    ):

        self.tour_id = tour_id
        self.title = title
        self.date = date
        self.price = price
        self.max_capacity = max_capacity
        self.created_by = created_by
        self.description = description
        self.location = location
        self.is_active = is_active
        # self.add_tour_to_list_of_tours() denne er flyttet til tour_controller

    def find_tour_id(self, cur):
        # conn, cur = connect_to_db()
        # Definerer SQL
        sql = """ SELECT COUNT(id) FROM tours """
        # Definerer touren
        # Sender SQL statementen og touren inn i databasen
        cur.execute(sql)
        sql_result = cur.fetchone()
        tour_id = sql_result[0]

        return tour_id

    def get_id(self):
        return str(self.tour_id)

    def add_tour_to_list_of_tours(self, cur):
        self.id = self.find_tour_id(cur)

        silly_dictionary = {
            "id": self.tour_id,
            "title": str(self.title),
            "date": str(self.date),
            "price": str(self.price),
            "max_capacity": str(self.max_capacity),
            "created_by": str(self.created_by),
            "description": str(self.description),
            "location": str(self.location),
        }
        list_of_tours.append(silly_dictionary)

    def update_tour_info(self, conn, cur, title, date, price, max_capacity, description, location):
        # Metode for å oppdatere infoen på brukerprofilen
        if title != "":
            self.title = title
            self.update_tour_value_in_db(conn, cur, "title", title)

        if max_capacity != "":
            self.max_capacity = max_capacity
            self.update_tour_value_in_db(conn, cur, "max_capacity", max_capacity)

        if description != "":
            self.description = description
            self.update_tour_value_in_db(conn, cur, "description", description)

        if location != "":
            self.location = location
            self.update_tour_value_in_db(conn, cur, "location", location)

        if date != "":
            self.date = date
            self.update_tour_value_in_db(conn, cur, "date", date)

        if price != "":
            self.price = price
            self.update_tour_value_in_db(conn, cur, "price", price)


    def update_tour_value_in_db(self, conn, cur, key, new_value):
        # key - hvilken kolonne du vil forandre. Må være string.
        # new_value - hva du vil verdien skal være

        # Må omforme key til å bli "key" slik at det fungerer med sql-spørringen
        fixed_key = f'"{key}"'

        try:
            update_pass = f"UPDATE tours SET {fixed_key} = ? WHERE id = ?"
            variables = (new_value, self.get_id())
            cur.execute(update_pass, variables)
            conn.commit()
        except Exception as e:
            pass


# Globale metoder

def add_tourgoers_to_list_of_created_tours(tour_id_with_usernames, list_of_created_tours):
    for single_dict in tour_id_with_usernames:
        for item in single_dict.items():
            key = item[0]
            value = item[1]
            list_of_usernames = []
            for usernames in value:
                for username in usernames:
                    list_of_usernames.append(username)

            for tour in list_of_created_tours:
                if tour['id'] == key:
                    tour['booked_by'] = list_of_usernames
    return list_of_created_tours


def add_spots_available_to_list_of_created_tours(list_of_created_tours):
    for created_tour in list_of_created_tours:
        for tour in list_of_tours:
            if tour['id'] == created_tour['id']:
                if 'spots_available' not in tour:
                    created_tour['spots_available'] = created_tour['max_capacity']
                else:
                    created_tour['spots_available'] = tour['spots_available']

    return list_of_created_tours


def mark_tour_as_inactive_in_list_of_tours(tour_id):
    for tour in list_of_tours:
        if str(tour['id']) == str(tour_id):
            tour['is_active'] = 0

