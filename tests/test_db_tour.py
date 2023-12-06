from application.model import tour
from application.model.dbtour import insert_tour_to_db, delete_tour_by_id, add_tour_to_list_from_db, \
    update_tour_is_active, get_tour_by_id, mark_tour_as_inactive_in_db, update_plasser_ledig
from application.model.dbuser import get_row_from_users
from application.model.dbbooking import create_booking
from application.model.tour import list_of_tours, Tour
from test_fixtures import setup_test_database, connect_test_db, cleanup_test_database, example_tour_1, example_tour_2

# Tester krav 2.1.1 og 9.1.2
def test_inserting_user_into_test_db(connect_test_db):
    conn, cur = connect_test_db
    # Sender inn "et objekt" til test db
    insert_tour_to_db(conn, cur, "Testtittel", 20, "Testdescription", "Testlocation", "Testdate", 100, 1)


    # Henter ut fra test db
    # Skriv om til funksjon
    sql = '''SELECT * FROM tours'''
    cur.execute(sql)
    result = cur.fetchone()

    # Lager enkeltvariabler som jeg kjører en assert mot
    expected_title = "Testtittel"
    expected_max_capacity = 20
    expected_description = "Testdescription"
    expected_location = "Testlocation"
    expected_date = "Testdate"
    expected_price = 100
    expected_created_by = 1

    # Må konvertere max_capacity, price, og created_by til int, fordi det som blir hentet ut fra db kommer som string
    # Så sjekker vi om alle instansvariabelene til "objektet" stemmer med det osm er i test db
    assert result is not None
    assert result[1] == expected_title
    assert int(result[2]) == expected_max_capacity
    assert result[3] == expected_description
    assert result[4] == expected_location
    assert result[5] == expected_date
    assert int(result[6]) == expected_price
    assert int(result[7]) == expected_created_by

# Tester krav 2.4.4
def test_tour_not_active(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Testtittel", 20, "Testdescription", "Testlocation", "Testdate", 100, 1)
    tour_id = 1
    # bruker funksjonen som er skrevet i dbtour for å "slette" eller gjøre innaktiv
    update_tour_is_active(conn, cur, tour_id)
    sql = '''SELECT is_active from tours where id = ?'''
    id = 1
    cur.execute(sql,(id,))
    is_active = cur.fetchone()

    assert is_active[0] == 0

# Tester krav 2.1.1 og 9.1.2
def test_is_active_tour_by_id_from_database(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Delete_tour_by_id", 11, "Testdescription", "Testlocation", "Testdate", 100, 2)
    update_tour_is_active(conn, cur, 1)
    tour = get_tour_by_id(cur, 1)

    assert tour.is_active == False

# Tester krav 2.2
def test_to_update_tour(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Testtittel", 20, "Testdescription", "Testlocation", "Testdate", 100, 1)

    tour = get_tour_by_id(cur, 1)

    tour.update_tour_info(conn, cur, "new title", "12.01.2024", 250, 120, "Hvordan lage mat på bålet", "Steigen")
    assert tour.tour_id == 1
    assert tour.title == "new title"
    assert tour.date == "12.01.2024"
    assert tour.price == 250
    assert tour.max_capacity == 120
    assert tour.description == "Hvordan lage mat på bålet"
    assert tour.location == "Steigen"

# Tester krav 2.1.1 og 9.1.2
def test_get_tour_by_id(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Testtittel", 20, "Testdescription", "Testlocation", "Testdate", 100, 1)

    tour = get_tour_by_id(cur, 1)

    assert tour is not None
    assert tour.tour_id == 1

# Tester krav 2.1.1 og 9.1.2
def test_tour_is_not_same(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "testnotsame", 22, "testdescript", "testlocation", "testdate", 200, 2)

    tour = get_tour_by_id(cur, 1)
    assert tour is not None
    assert tour.tour_id != 2

# Tester krav 2.2
def test_update_tour_with_empty_values(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Testtittel", 20, "Testdescription", "Testlocation", "Testdate", 100, 1)
    tour = get_tour_by_id(cur, 1)
    tour.update_tour_info(conn, cur, "", "", "", "", "", "")

    assert tour.tour_id == tour.tour_id
    assert tour.title == tour.title
    assert tour.date == tour.date
    assert tour.price == tour.price
    assert tour.max_capacity == tour.max_capacity
    assert tour.description == tour.description
    assert tour.location == tour.location

# Tester krav 2.1.1 og 9.1.2
def test_get_tour_when_id_doesnt_exist(connect_test_db):
    conn, cur = connect_test_db
    tour = get_tour_by_id(cur, 99)
    assert tour is None

# Tester krav 2.4.4
def test_delete_tour_by_id(connect_test_db):
    conn, cur = connect_test_db

    insert_tour_to_db(conn, cur, "Tour to be deactivated", 20, "Description", "Location", "2023-01-01", 100, 1)
    tour = get_tour_by_id(cur, 1)
    delete_tour_by_id(conn, cur, 1)
    deactivated_tour = get_tour_by_id(cur, 1)

    assert deactivated_tour is not None
    assert deactivated_tour.is_active == 0

    assert deactivated_tour.title == tour.title

# Tester krav 2.1.1 og 9.1.2
def test_find_tour_id(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Test Tour", 10, "Test Description", "Test Location", "2023-01-01", 50, 1)
    tour_1 = get_tour_by_id(cur, 1)

    assert tour_1.tour_id != 0
    assert tour_1.tour_id == 1

# Tester krav 2.1.1 og 9.1.2
def test_find_tour_id_when_multiple_tours_in_database(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Test Tour", 10, "Test Description", "Test Location", "2023-01-01", 50, 1)
    tour_1 = get_tour_by_id(cur, 1)

    assert tour_1.tour_id != 0
    assert tour_1.tour_id == 1

    insert_tour_to_db(conn, cur, "Another Tour", 15, "Another Description", "Another Location", "2023-02-01", 75, 2)
    tour_2 = get_tour_by_id(cur, 2)

    assert tour_2.tour_id == 2
    assert tour_2.tour_id != tour_1.tour_id

# Tester krav 2.5.1
def test_add_mulitple_tours_to_list_of_tours(connect_test_db):
    list_of_tours.clear()
    conn, cur = connect_test_db
    tour1 = Tour(1, "Fæsking i Saltstraumen", "none", 200, 30, 1, "Kveitefiske i Saltstraumen", "Saltstraumen")
    tour2 = Tour(2, "Fisking i Saltstraumen", "none", 200, 30, 1, "Kveitefiske i Saltstraumen", "Saltstraumen")

    tour1.add_tour_to_list_of_tours(cur)
    initial_length = len(list_of_tours)
    tour2.add_tour_to_list_of_tours(cur)

    assert len(list_of_tours) == initial_length + 1
    assert len(list_of_tours) == 2

    list_of_tours.clear()

# Tester krav 2.4.4
def test_mark_tour_as_inactive_in_db(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Test Tour", 10, "Test Description", "Test Location", "2023-01-01", 50, 1)
    tour1 = get_tour_by_id(cur, 1)
    assert tour1.is_active == True

    mark_tour_as_inactive_in_db(cur, conn, 1)
    tour2 = get_tour_by_id(cur, 1)

    assert tour2.is_active == False

# Tester krav 2.4.4
def test_mark_tour_as_inactive_if_tour_doesnt_exist(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Test Tour", 10, "Test Description", "Test Location", "2023-01-01", 50, 1)
    tour1 = get_tour_by_id(cur, 1)
    assert tour1.is_active == True

    mark_tour_as_inactive_in_db(cur, conn, 4)
    tour4 = get_tour_by_id(cur, 4)

    assert tour1.is_active == True
    assert tour4 is None

# Tester krav 2.5.1
def test_update_plasser_ledig_subtracts_properly(connect_test_db):
    list_of_tours.clear()
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Test Tour", 10, "Test Description", "Test Location", "2023-01-01", 50, 1)
    tour = get_tour_by_id(cur, 1)
    tour.add_tour_to_list_of_tours(cur)
    max_capacity = list_of_tours[0]['max_capacity']
    assert int(max_capacity) == 10

    create_booking(conn, cur, 2, 1, 3)
    create_booking(conn, cur, 3, 1, 4)
    bookings_made = 7
    update_plasser_ledig(cur)

    available_slots = list_of_tours[0]['spots_available']
    assert int(available_slots) == int(max_capacity) - bookings_made

    list_of_tours.clear()

# Tester krav 2.5.1
def test_add_tour_to_list_when_just_one_tour_in_database(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Test Tour", 10, "Test Description", "Test Location", "2023-01-01", 50, 1)

    add_tour_to_list_from_db(cur)

    length_of_list = len(list_of_tours)

    assert length_of_list == 1
    assert length_of_list != 0

    list_of_tours.clear()

# Tester krav 2.5.1
def test_add_tour_to_list_when_multiple_tours_in_db(connect_test_db):
    conn, cur = connect_test_db
    insert_tour_to_db(conn, cur, "Test Tour", 10, "Test Description", "Test Location", "2023-01-01", 50, 1)
    insert_tour_to_db(conn, cur, "Test Tour2", 10, "Test Description2", "Test Location", "2023-01-01", 50, 1)
    insert_tour_to_db(conn, cur, "Test Tour3", 10, "Test Description3", "Test Location", "2023-01-01", 50, 1)

    add_tour_to_list_from_db(cur)

    length_of_list = len(list_of_tours)

    assert length_of_list == 3

    list_of_tours.clear()






