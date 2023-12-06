list_of_bookings = []


# [x] Tested
# - if it returns correct values
def get_rows_bookings(cur):
    sql = '''SELECT COUNT(id) FROM booking'''
    cur.execute(sql)
    result = cur.fetchone()
    number_bookings = result[0]

    return number_bookings


# [x] Tested
# - if it adds info (correctly) to the database
def create_booking(conn, cur, user_id, tour_id, participants):
    create_new_row_sql = "INSERT INTO booking(id_user, id_tour, participants, is_active) VALUES(?,?,?,true)"
    sql_vars = (str(user_id), str(tour_id), int(participants))
    cur.execute(create_new_row_sql, sql_vars)
    conn.commit()


# [x] Tested
# - If it adds correct info
# - If it adds duplicate info
def update_list_of_bookings(cur):
    sql = "SELECT * FROM booking"
    cur.execute(sql)
    info_retrieved = cur.fetchall()

    for tuple in info_retrieved:
        temp_dict = {
            "id": tuple[0],
            "id_user": tuple[1],
            "id_tour": tuple[2],
            "participants": tuple[3],
            "is_active": tuple[4],
        }
        if temp_dict not in list_of_bookings:
            list_of_bookings.append(temp_dict)


# [x]  Tested
# - Henter riktige id-er hvor is_active == true
def get_users_from_bookings(cur, tour_id):
    sql = f'''SELECT * FROM booking WHERE id_tour = {str(tour_id)} AND is_active = true'''
    cur.execute(sql)
    all_bookings = cur.fetchall()

    list_of_user_ids = []
    for booking in all_bookings:
        user_id = booking[1]
        list_of_user_ids.append(user_id)

    return list_of_user_ids


# [x] Tested
def find_all_usernames_for_tour(cur, current_users_tour_ids):
    username_dictionaries_list = []

    for tour_id in current_users_tour_ids:
        users_in_tour = get_users_from_bookings(cur, tour_id)
        list_of_users = []
        for user_id in users_in_tour:
            sql = '''SELECT username FROM users WHERE id = ?'''
            cur.execute(sql, user_id, )
            username = cur.fetchone()
            list_of_users.append(username)
        dict_entry = {tour_id: list_of_users}
        username_dictionaries_list.append(dict_entry)
    return username_dictionaries_list


# [x] Tested
def mark_all_bookings_from_specific_tour_as_inactive_in_db(cur, conn, tour_id):
    sql = f'''UPDATE booking SET is_active = False WHERE id_tour = {str(tour_id)}'''
    cur.execute(sql)
    conn.commit()


# [x] Tested
def check_if_participants_exceed_max_capacity(cur, tour_id, new_participants):
    # Returns True if participants exceed max capacity
    # Else returns False
    sql = f'''SELECT participants FROM booking WHERE is_active = 1 AND id_tour = {tour_id}'''
    cur.execute(sql)
    participants_tuple = cur.fetchall()

    active_participants = 0
    for x in participants_tuple:
        active_participants += x[0]

    sql = f'''SELECT max_capacity FROM tours WHERE id = {tour_id}'''
    cur.execute(sql)

    max_capacity = cur.fetchone()

    total_participants = new_participants + active_participants

    return_value = False
    if total_participants > max_capacity[0]:
        return_value = True
    return return_value


# [x] Tested
def mark_booking_as_inactive(cur, conn, user_id, tour_id):
    sql = f'''UPDATE booking SET is_active = false WHERE id_user = {str(user_id)} AND id_tour = {str(tour_id)}'''
    cur.execute(sql)
    conn.commit()


# [x] Tested
def add_plasser_ledig_to_correct_bookings(cur, correct_bookings):
    # Correct Bookings bør allerede eksistere.
    # Går gjennom alle correct bookings, søker opp i sql hvor mange participants
    # det er (som har is_active = true) og trekker dette fra max_capacity
    # for å finne ut av hvor mange plasser som er ledige
    for dictionary in correct_bookings:
        sql = f'''SELECT participants FROM booking WHERE is_active = True AND id_tour = {dictionary["id_tour"]}'''
        cur.execute(sql)
        participants_tuple = cur.fetchall()
        active_participants = 0
        for x in participants_tuple:
            active_participants += x[0]
        ledige_plasser = int(dictionary['max_capacity']) - active_participants
        dictionary['spots_available'] = ledige_plasser

    return correct_bookings


# [ ] Tested

def update_participants_in_booking(conn, cur, tour_id, user_id, participants):
    sql = '''SELECT SUM(participants) FROM booking WHERE id_user = ? AND id_tour = ?'''
    values = (user_id, tour_id)
    cur.execute(sql, values)
    result = cur.fetchone()
    current_participants = result[0]

    total_participants = current_participants + participants

    sql2 = '''UPDATE booking SET participants = ? WHERE id_user = ? AND id_tour = ?'''
    values2 = (total_participants, user_id, tour_id)
    cur.execute(sql2, values2)
    conn.commit()

    return total_participants


# [ ] Tested
def update_booking(conn, cur, user_id, tour_id, participants):
    check_if_already_exists = "SELECT * FROM booking WHERE id_user = ? AND id_tour = ?"
    sql_vars = (user_id, tour_id)
    cur.execute(check_if_already_exists, sql_vars)
    existing_data = cur.fetchone()

    # If data already exists, but is_active is false, reset data.
    if existing_data[4] == 0:
        sql = '''UPDATE booking SET is_active = 1 WHERE id_user = ? AND id_tour = ?'''
        cur.execute(sql, sql_vars)
        sql = '''UPDATE booking SET participants = 0 WHERE id_user = ? AND id_tour = ?'''
        cur.execute(sql, sql_vars)
        conn.commit()

    if user_id == int(existing_data[1]) and tour_id == int(existing_data[2]):
        update_participants_in_booking(conn, cur, tour_id, user_id, participants)


# [x] Tested
# - returns True if data exists
# - returns False if data does not exist
def check_for_existing_booking(cur, user_id, tour_id):
    # Sjekker om bruker allerede har booket tour til denne touren
    check_if_already_exists = "SELECT * FROM booking WHERE id_user = ? AND id_tour = ?"
    sql_vars = (user_id, tour_id)
    cur.execute(check_if_already_exists, sql_vars)
    existing_data = cur.fetchone()

    if existing_data:
        return True
    else:
        return False


# [x] tested
def find_info_about_tours_user_has_booked(cur, user_id):
    correct_bookings = []

    sql = f'''SELECT * FROM booking WHERE id_user = {str(user_id)} AND is_active = 1'''
    cur.execute(sql)
    booking_info = cur.fetchall()
    # booking_info -> [(7, '1', '10', 10, 1)]
    # booking_info[x][1] -> id_user (str)
    # booking_info[x][2] -> id_tour (str)
    # booking_info[x][3] -> participants (int)

    for entry in booking_info:
        temp_dict = {
            'id_user': entry[1],
            'id_tour': entry[2],
            'participants': entry[3],
        }
        correct_bookings.append(temp_dict)

    # finn info i tours
    # tour_info -> [(10, 'please_work_2', 10, 'asd', 'asd', 'asd', 100, '3', 1, None)]
    for item in booking_info:
        sql = f'''SELECT * FROM tours WHERE id = {int(item[2])}'''
        cur.execute(sql)
        tour_info = cur.fetchall()

        for info in tour_info:
            for booking in correct_bookings:
                if str(info[0]) == str(booking['id_tour']):
                    booking['tour_title'] = info[1]
                    booking['max_capacity'] = info[2]
                    booking['description'] = info[3]
                    booking['location'] = info[4]
                    booking['date'] = info[5]
                    booking['price'] = info[6]
                    booking['created_by'] = info[7]

    return correct_bookings


# [x] tested
# - if it marks all bookings with specific id as inactive
def mark_all_bookings_from_specific_tour_as_inactive_in_list(tour_id):
    for booking in list_of_bookings:
        if str(booking['id_tour']) == str(tour_id):
            booking['is_active'] = 0
