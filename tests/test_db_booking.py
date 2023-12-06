from application.model.dbbooking import create_booking, get_rows_bookings, update_list_of_bookings, \
    check_for_existing_booking, list_of_bookings, mark_all_bookings_from_specific_tour_as_inactive_in_list, \
    mark_booking_as_inactive, get_users_from_bookings, mark_all_bookings_from_specific_tour_as_inactive_in_db, \
    check_if_participants_exceed_max_capacity, find_info_about_tours_user_has_booked, find_all_usernames_for_tour, \
    add_plasser_ledig_to_correct_bookings, update_participants_in_booking, update_booking

from application.model.dbtour import insert_tour_to_db
from application.model.dbuser import insert_user_info_to_db
from application.model.user import get_tours_from_specific_user, get_tour_ids_from_tours_from_specific_user
from test_fixtures import setup_test_database, connect_test_db, cleanup_test_database

# Tester krav 3.1.1 og 9.1.3
def test_inserting_booking_into_test_db(connect_test_db):
    conn, cur = connect_test_db
    create_booking(conn, cur, 1, 1, 4)

    sql = '''SELECT * FROM booking'''
    cur.execute(sql)
    result = cur.fetchone()

    expected_userid = 1
    expected_tourid = 1
    expected_participants = 4

    # Use assert to check if the retrieved data matches the expected values
    assert result is not None  # Ensure that data was retrieved
    assert int(result[1]) == expected_userid
    assert int(result[2]) == expected_tourid
    assert int(result[3]) == expected_participants

# Tester krav 3.1.1 og 9.1.3
def test_check_for_booking_exist_in_db(connect_test_db):
    conn, cur = connect_test_db
    create_booking(conn, cur, 1, 1, 12)
    result_existing = check_for_existing_booking(cur, 1, 1)

    assert result_existing is True


def test_does_get_rows_booking_return_correct_values(connect_test_db):
    conn, cur = connect_test_db
    this_should_be_0 = get_rows_bookings(cur)
    create_booking(conn, cur, 1, 1, 4)
    this_should_be_1 = get_rows_bookings(cur)
    for x in range(5):
        create_booking(conn, cur, x, x, x)
    this_should_be_6 = get_rows_bookings(cur)

    assert this_should_be_0 == 0
    assert this_should_be_1 == 1
    assert this_should_be_6 == 6

# Tester krav 3.1.1 og 9.1.3
def test_create_booking_adds_values_to_database(connect_test_db):
    conn, cur = connect_test_db
    create_booking(conn, cur, 1, 11, 111)

    # Mener å huske at det ikke er riktig å 'lage nye funksjoner'
    # eller 'skrive nye database spørringer' i tester, men har ikke
    # funksjon som henter all data fra booking tabellen, så skriver den her.
    sql = '''SELECT * FROM booking'''
    cur.execute(sql)
    database_results = cur.fetchall()

    id_user = database_results[0][1]
    id_tour = database_results[0][2]
    participants = database_results[0][3]

    assert id_user == '1'
    assert id_tour == '11'
    assert participants == 111

# Tester krav 3.2
def test_update_list_of_bookings_adds_data_to_list_of_bookings(connect_test_db):
    amount_of_elements_in_list_of_booking_before = len(list_of_bookings)

    conn, cur = connect_test_db
    create_booking(conn, cur, 1, 11, 111)
    create_booking(conn, cur, 2, 22, 222)
    update_list_of_bookings(cur)

    amount_of_elements_in_list_of_booking_after = len(list_of_bookings)

    assert amount_of_elements_in_list_of_booking_before == 0
    assert amount_of_elements_in_list_of_booking_after == 2
    list_of_bookings.clear()

# Tester krav 3.2
def test_update_list_of_bookings_adds_correct_data_to_list_of_bookings(connect_test_db):
    conn, cur = connect_test_db
    create_booking(conn, cur, 1, 11, 111)
    update_list_of_bookings(cur)

    assert list_of_bookings[0]['id'] == 1
    assert list_of_bookings[0]['id_user'] == '1'
    assert list_of_bookings[0]['id_tour'] == '11'
    assert list_of_bookings[0]['participants'] == 111
    list_of_bookings.clear()

# Tester krav 3.2
def test_update_list_of_bookings_does_not_add_duplicate_info(connect_test_db):
    list_of_bookings.append({
        'id': 1,
        'id_tour': '11',
        'id_user': '1',
        'is_active': 1,
        'participants': 111
    })

    conn, cur = connect_test_db
    create_booking(conn, cur, 1, 11, 111)
    update_list_of_bookings(cur)
    assert len(list_of_bookings) == 1
    list_of_bookings.clear()


# Tester krav 3.2
def test_does_mark_all_bookings_from_specific_tour_as_inactive_in_list_work(connect_test_db):
    list_of_bookings.append({'id': 1, 'id_tour': '11', 'id_user': '1', 'is_active': 1, 'participants': 5})
    list_of_bookings.append({'id': 1, 'id_tour': '11', 'id_user': '5', 'is_active': 1, 'participants': 2})
    booking_1 = list_of_bookings[0]
    booking_2 = list_of_bookings[1]
    assert booking_1['is_active'] == 1
    assert booking_2['is_active'] == 1
    mark_all_bookings_from_specific_tour_as_inactive_in_list('11')
    booking_1 = list_of_bookings[0]
    booking_2 = list_of_bookings[1]
    list_of_bookings.clear()
    assert booking_1['is_active'] == 0
    assert booking_2['is_active'] == 0

# Tester krav 3.2
def test_get_users_from_bookings_only_returns_active_bookings(connect_test_db):
    conn, cur = connect_test_db

    # Lager 4 bookings - alle til samme tour_id (1)
    create_booking(conn, cur, 1, 1, 1)  # 1
    create_booking(conn, cur, 2, 1, 2)  # 2
    create_booking(conn, cur, 3, 1, 3)  # 3
    create_booking(conn, cur, 4, 1, 4)  # 4
    # Gjør booking 2 og 4 inaktive
    mark_booking_as_inactive(cur, conn, 2, 1)
    mark_booking_as_inactive(cur, conn, 4, 1)
    # Henter tours med get_users_from_bookings
    list_of_user_ids = get_users_from_bookings(cur, 1)

    # Assert
    assert list_of_user_ids == ['1', '3']

# Tester krav 3.1.1 og 9.1.3
def test_check_for_existing_booking_returns_correct_values(connect_test_db):
    conn, cur = connect_test_db

    # Creating one tour that already exists
    create_booking(conn, cur, 1, 1, 1)

    assert check_for_existing_booking(cur, 1, 1) is True
    assert check_for_existing_booking(cur, 1, 2) is False
    assert check_for_existing_booking(cur, 2, 1) is False

# Tester krav 3.1.4
def test_mark_booking_as_inactive_marks_correct_booking_as_inactive(connect_test_db):
    conn, cur = connect_test_db
    create_booking(conn, cur, 1, 10, 1)  # 1
    create_booking(conn, cur, 2, 10, 1)  # 2
    create_booking(conn, cur, 1, 20, 1)  # 3
    create_booking(conn, cur, 2, 20, 1)  # 4

    mark_booking_as_inactive(cur, conn, 1, 10)  # marks 1 as inactive
    mark_booking_as_inactive(cur, conn, 2, 20)  # marks 4 as inactive

    update_list_of_bookings(cur)
    assert list_of_bookings[0]['id_tour'] == '10' and list_of_bookings[0]['id_user'] == '1' and \
           list_of_bookings[0]['is_active'] == 0
    assert list_of_bookings[1]['id_tour'] == '10' and list_of_bookings[1]['id_user'] == '2' and \
           list_of_bookings[1]['is_active'] == 1
    assert list_of_bookings[2]['id_tour'] == '20' and list_of_bookings[2]['id_user'] == '1' and \
           list_of_bookings[2]['is_active'] == 1
    assert list_of_bookings[3]['id_tour'] == '20' and list_of_bookings[3]['id_user'] == '2' and \
           list_of_bookings[3]['is_active'] == 0
    list_of_bookings.clear()

# Tester krav 3.2
def test_mark_all_bookings_from_specific_tour_as_inactive_in_db(connect_test_db):
    conn, cur = connect_test_db

    create_booking(conn, cur, 1, 10, 1)  # 1
    create_booking(conn, cur, 2, 10, 1)  # 2
    create_booking(conn, cur, 1, 20, 1)  # 3
    create_booking(conn, cur, 2, 20, 1)  # 4

    mark_all_bookings_from_specific_tour_as_inactive_in_db(cur, conn, 10)

    update_list_of_bookings(cur)
    assert list_of_bookings[0]['id_tour'] == '10' and list_of_bookings[0]['id_user'] == '1' and \
           list_of_bookings[0]['is_active'] == 0
    assert list_of_bookings[1]['id_tour'] == '10' and list_of_bookings[1]['id_user'] == '2' and \
           list_of_bookings[1]['is_active'] == 0
    assert list_of_bookings[2]['id_tour'] == '20' and list_of_bookings[2]['id_user'] == '1' and \
           list_of_bookings[2]['is_active'] == 1
    assert list_of_bookings[3]['id_tour'] == '20' and list_of_bookings[3]['id_user'] == '2' and \
           list_of_bookings[3]['is_active'] == 1
    list_of_bookings.clear()

# Tester krav 3.1.1
def test_check_if_participants_exceed_max_capacity(connect_test_db):
    conn, cur = connect_test_db
    # tour_id = 1
    insert_tour_to_db(conn, cur, "title_1", 10, "desc_1", "loc_1", "date_1",
                      1000, 1)
    # tour_id = 2
    insert_tour_to_db(conn, cur, "title_2", 5, "desc_2", "loc_2", "date_2",
                      1000, 1)

    create_booking(conn, cur, 1, 2, 3)

    assert check_if_participants_exceed_max_capacity(cur, 1, 11) is True
    assert check_if_participants_exceed_max_capacity(cur, 1, 10) is False
    assert check_if_participants_exceed_max_capacity(cur, 2, 5) is True
    assert check_if_participants_exceed_max_capacity(cur, 2, 2) is False

# Tester krav 3.2
def test_find_info_about_tours_user_has_booked_returns_correct_info(connect_test_db):
    conn, cur = connect_test_db

    # Create Tours & Bookings for these tours
    # tour_id = 1
    insert_tour_to_db(conn, cur, "title_1", 10, "desc_1", "loc_1",
                      "date_1", 1000, 1)
    # tour_id = 2
    insert_tour_to_db(conn, cur, "title_2", 5, "desc_2", "loc_2",
                      "date_2", 1000, 1)
    # tour_id = 1
    create_booking(conn, cur, 1, 1, 2)
    create_booking(conn, cur, 2, 1, 3)
    # tour_id = 2
    create_booking(conn, cur, 1, 2, 5)

    tours_user_1_has_booked = find_info_about_tours_user_has_booked(cur, 1)
    tours_user_2_has_booked = find_info_about_tours_user_has_booked(cur, 2)

    user_1_tour_should_look_like = [{'created_by': '1', 'date': 'date_1', 'description': 'desc_1',
                                     'id_tour': '1', 'id_user': '1', 'location': 'loc_1',
                                     'max_capacity': 10, 'participants': 2, 'price': 1000,
                                     'tour_title': 'title_1'},
                                    {'created_by': '1', 'date': 'date_2', 'description': 'desc_2',
                                     'id_tour': '2', 'id_user': '1', 'location': 'loc_2',
                                     'max_capacity': 5, 'participants': 5, 'price': 1000,
                                     'tour_title': 'title_2'}]

    user_2_tour_should_look_like = [{'created_by': '1', 'date': 'date_1', 'description': 'desc_1',
                                     'id_tour': '1', 'id_user': '2', 'location': 'loc_1', 'max_capacity': 10,
                                     'participants': 3, 'price': 1000, 'tour_title': 'title_1'}]

    assert tours_user_1_has_booked == user_1_tour_should_look_like
    assert len(tours_user_1_has_booked) == 2
    assert tours_user_2_has_booked == user_2_tour_should_look_like
    assert len(tours_user_2_has_booked) == 1


def test_find_all_usernames_for_tour_finds_usernames(connect_test_db):
    conn, cur = connect_test_db

    # ---Create User---
    # user_id = 1
    # This is the user that created the tours
    insert_user_info_to_db(conn, cur, "Petter Svart", "123", "user1@gmail.com")
    # user_id = 2
    # This users tours should not be shown
    insert_user_info_to_db(conn, cur, "Ola Nordmann", "P_notUsed", "E_notUsed")
    # ---Create Tour---
    # tour_id = 1 -> created by Petter Svart
    insert_tour_to_db(conn, cur, "title_1", 10, "desc_1", "loc_1",
                      "date_1", 1000, 1)
    # tour_id = 2 -> created by Petter Svart
    insert_tour_to_db(conn, cur, "title_2", 5, "desc_2", "loc_2",
                      "date_2", 1000, 1)
    # tour_id = 3 -> created by Ola Nordmann
    insert_tour_to_db(conn, cur, "T_notUsed", 5, "D_notUsed", "L_notUsed",
                      "D_notUsed", 1000, 2)
    # ---Create Booking---
    # Petter Svart & Ola Nordmann books title_1
    create_booking(conn, cur, 1, 1, 1)
    create_booking(conn, cur, 2, 1, 1)
    # Ola Nordmann books title_2 & T_notUsed
    create_booking(conn, cur, 2, 2, 1)
    create_booking(conn, cur, 2, 3, 1)

    # --- Create a dictionary of tour_ids & usernames ---
    # [ { user_id: [(username), (username)] } ]
    # [{1: [('Petter Svart',), ('Ola Nordmann',)]}, {2: [('Ola Nordmann',)]}]

    # finds all tours Petter Svart made
    list_of_created_tours = get_tours_from_specific_user(cur, 1)
    # extracts only the tour ids from these tours
    current_users_tour_ids = get_tour_ids_from_tours_from_specific_user(list_of_created_tours)
    # finds the usernames of the users that booked those tours, returns dict
    # that hopefully looks like how i defined it in comment above
    tour_id_with_usernames = find_all_usernames_for_tour(cur, current_users_tour_ids)

    assert tour_id_with_usernames == [{1: [('Petter Svart',), ('Ola Nordmann',)]}, {2: [('Ola Nordmann',)]}]
    assert len(tour_id_with_usernames) == 2
    list_of_bookings.clear()


def test_add_plasser_ledig_to_correct_bookings(connect_test_db):
    conn, cur = connect_test_db
    # ---create tours---
    # tour_id = 1
    insert_tour_to_db(conn, cur, "title_1", 10, "desc_1", "loc_1",
                      "date_1", 1000, 1)
    # tour_id = 2
    insert_tour_to_db(conn, cur, "title_2", 5, "desc_2", "loc_2",
                      "date_2", 1000, 1)

    # ---create bookings for these tours (2)---
    create_booking(conn, cur, 1, 1, 4)  # tour 1 -> 10 - 4 = 6
    create_booking(conn, cur, 2, 1, 2)  # tour 1 -> 6 - 2  = 4 <-
    create_booking(conn, cur, 1, 2, 2)  # tour 2 -> 5 - 2  = 3
    create_booking(conn, cur, 3, 2, 1)  # tour 2 -> 3 - 1  = 2 <-

    # ---create correct_bookings---
    correct_bookings = find_info_about_tours_user_has_booked(cur, 1)
    correct_bookings = add_plasser_ledig_to_correct_bookings(cur, correct_bookings)

    assert correct_bookings[0]['spots_available'] == 4
    assert correct_bookings[1]['spots_available'] == 2
    list_of_bookings.clear()


def test_update_participants_in_booking_for_cancelled_booking(connect_test_db):
    conn, cur = connect_test_db
    # create booking
    create_booking(conn, cur, 1, 1, 2)
    first_created = find_info_about_tours_user_has_booked(cur, 1)
    # cancel it
    mark_booking_as_inactive(cur, conn, 1, 1)
    # re-book
    update_booking(conn, cur, 1, 1, 4)
    last_created = find_info_about_tours_user_has_booked(cur, 1)

    assert first_created[0]['participants'] == 2
    assert last_created[0]['participants'] == 4
    list_of_bookings.clear()
